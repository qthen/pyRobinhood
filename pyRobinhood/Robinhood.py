'''
Main class for interacting with Robinhood API, wraps the Robinhood API and
queries.
'''

from pyRobinhood.Order import Order
from pyRobinhood.RobinhoodAPI import RobinhoodAPI
from pyRobinhood.Endpoints import Endpoints
from pyRobinhood.exceptions import LoginError, SymbolNotFound, APIError, NotLoggedIn, OrderFailed, OrderMayCauseDayTrade

class Robinhood(object):

	'''
	Creates an instance that interacts with the Robinhood API and exposes
	common front end operations. Loads the environment constants from
	ConfigService (so construction can fail). 
	Inputs: 
		timeout (Int) - Timeout for API requests.
	'''
	def __init__(self, timeout = 15):
		self._robinhood_api = RobinhoodAPI(timeout=timeout)

		self.CLIENT_ID = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"

		# The token returned from a login request. 
		self.TOKEN = None

		# The current username of the logged in user for this instance.
		self.USERNAME = None


	'''
	Checks if the current Robinhood instance is logged in.
	Returns:
		(bool)
	'''
	def logged_in(self):
		return self.TOKEN is not None

	'''
	Request a token from the front end to use for methods that require
	authentication 
	Inputs: 
		username (String) - The username to login with.
		password (String) - The password to login with. 
	Returns: 
		bool - True if login successful 
	Throws: 
		LoginError - When login is not successful
	'''
	def login(self, username, password):
		payload = {
			'username': username,
			'password': password,
			'client_id': self.CLIENT_ID,
			'grant_type': 'password',
			'scope': 'internal'
		}

		headers = {}

		try:
			result = self._robinhood_api.query(Endpoints.LOGIN, payload, 
				headers)
			self.TOKEN = result['access_token']
			self.USERNAME = username
			return True
		except APIError:
			raise LoginError("Robinhood API returned non-200 status code.")

	'''
	Logs the current user out.
	Returns:
		(bool)
	Throws:
		NotLoggedIn
	'''
	def logout(self):
		if self.logged_in():
			headers = { 'Authorization': 'Bearer ' + self.TOKEN }
			r = requests.post("https://api.robinhood.com/oauth2/revoke_token/",
				headers=headers)
			if r.status_code == 200:
				return True
			else:
				raise APIError()
		else:
			raise NotLoggedIn()

	'''
	Places an order for some security.
	Input:
		symbol (String) - The symbol of the instrument to place an order on.
		type (String) - The type of order (market|limit).
		time_in_force (String) - gfd|gtc|ioc|opg.
		trigger (String) - immediate or stop.
		price (Float) - The price of order (max if buy, min if sell).
		stop_price (Float) - The price when a stop order triggers (only 
		relevant when trigger = 'stop')
		quantity (Int) - The number of shares involved in the transaction.
		side (String) - buy|sell.
		extended_hours (Bool) - Should execute during pre/after hours.
		override_day_trade_checks (Bool) - Override day trade warnings
	Returns:
		(Order) - Contains the information of the resulting order.
	Throws:
		OrderMayCauseDayTrade - If an order may cause a day trade as told by 
		Robinhood API.
	'''
	def _place_order(self, symbol, type, time_in_force, trigger, price,
		stop_price, quantity, side, extended_hours = True,
		override_day_trade_checks = False):
		if self.logged_in():
			instrument_url = self._instrument_url_by_symbol(symbol)
			account_url = self._account_url()

			payload = {
				'account': account_url,
				'instrument': instrument_url,
				'symbol': symbol,
				'type': type,
				'time_in_force': time_in_force,
				'trigger': trigger,
				'price': price,
				'stop_price': stop_price,
				'quantity': quantity,
				'side': side,
				'extended_hours': extended_hours,
				'override_day_trade_checks': override_day_trade_checks
			}
			headers = { 'Authorization': 'Bearer ' + self.TOKEN }

			try:
				result = self._robinhood_api.query(Endpoints.ORDERS, payload, headers)
			except APIError as e:
				# Placing an order typically results in an 201 status code, but error status codes can be returned. Here are the cases:
				if e.err_response and 'detail': in e.err_response and 
				e.err_response['detail'] == "Sell may cause day trade.":
					raise OrderMayCauseDayTrade()
				else:
					raise OrderFailed("Order failed since API returned an error. Dump: {}".format(e))

			if 'id' in result:
				return Order(result['id'], result['fees'], result['cancel'],
					result['cumulative_quantity'], result['reject_reason'],
					result['state'], result['url'], result['updated_at'],
					result['created_at'], result['average_price'])
			else:
				raise RuntimeError("Order was sent but failed to find the"\
					" id. Dump of order result: ".format(result))

		else:
			raise LoginError()

	'''
	Places a Robinhood MARKET BUY order.

	This method relies on the fact that fetching the last trade price from 
	Robinhood works (which is not guaranteed, there IS throttling - up to 300 
	seconds), thus you should always prefer limit orders where you must 
	explicitly specify a price.
	Inputs:
		symbol (String) - The symbol of the instrument to buy.
		quantity (Int) - The number of shares to buy.
		time_in_force (String) - gfd|gtc|ioc|opg.
		extended_hours (Bool) - Should execute during pre/after hours.
	'''
	def place_market_buy(self, symbol, quantity, time_in_force = 'gtc', extended_hours = True):
		if self.logged_in():
			# Market orders are limit orders with the price collared 5%, get the last trade price.
			symbol_quote = self.get_quote(symbol)
			try:
				result = self._place_order(symbol = symbol, type='market', 
					time_in_force = time_in_force, trigger = 'immediate', 
					price = symbol_quote.last_trade_price, stop_price = None,
					quantity = quantity, side = 'buy', 
					extended_hours = extended_hours)
			except APIError as e:
				# For some reason, market orders can return non-200 status code irrespective of the result of the order, check if the reject reason is null
				# if 'reject_reason' in e.err_response:
				pass

		else:
			raise LoginError()


	'''
	Places a Robinhood MARKET SELL order.
	'''
	def place_market_sell(self, symbol, quantity, time_in_force = 'gtc', 
		extended_hours = True):
		if self.logged_in():
			# Market orders are limit orders with the price collared 5%, get the last trade price.
			symbol_quote = self.get_quote(symbol)
			result = self._place_order(symbol = symbol, type='market',
				time_in_force = time_in_force, trigger = 'immediate',
				price = symbol_quote.last_trade_price, stop_price = None,
				quantity = quantity, side = 'sell',
				extended_hours = extended_hours)
		else:
			raise LoginError()

	'''
	Places a Robinhood LIMIT BUY order.
	'''
	def place_limit_buy(self, symbol, quantity, price, time_in_force = 'gtc', 
		extended_hours = True):
		if self.logged_in():
			result = self._place_order(symbol = symbol, type='limit',
				time_in_force = time_in_force, trigger = 'immediate',
				price = price, stop_price = None, quantity = quantity,
				side = 'buy', extended_hours = extended_hours)
		else:
			raise LoginError()

	'''
	Places a Robinhood LIMIT SELL order.
	'''
	def place_limit_sell(self, symbol, quantity, price, time_in_force = 'gtc', 
		extended_hours = True):
		if self.logged_in():
			result = self._place_order(symbol = symbol, type='limit',
				time_in_force = time_in_force, trigger = 'immediate',
				price = price, stop_price = None, quantity = quantity,
				side = 'sell', extended_hours = extended_hours)
		else:
			raise LoginError()

	'''
	Gets a quote of a given instrument by symbol.
	Inputs:
		symbol (String) - The symbol to look up.
	Returns:
		(Quote)
	'''
	def get_quote(self, symbol):
		payload = { 'symbol': "MSFT" }
		headers = {}
		result = self._robinhood_api.query(Endpoints.QUOTE, payload, headers)
		return Quote(result['ask_price'], result['ask_size'],
			result['bid_price'], result['bid_size'],
			result['last_trade_price'], 
			result['last_extended_hours_trade_price'],
			result['previous_close'], result['adjusted_previous_close'],
			result['previous_close_date'], result['symbol'],
			result['trading_halted'], result['updated_at'])

	'''
	Gets the account URL of the current logged in user.
	'''
	def _account_url(self):
		if self.logged_in():
			payload = {}
			headers = { 'Authorization': 'Bearer ' + self.TOKEN }

			# Results returns an array of results, despite the fact that there 
			# should be an one to one relationship for user to account url.
			result = self._robinhood_api.query(Endpoints.ACCOUNT, payload,
				headers)
			return result['results'][0]['url']

		else:
			raise NotLoggedIn("Need to be logged in to get account id.")

	'''
	Gets the portfolio positions
	'''

	'''
	Given a symbol, returns the instrument info as a dict.
	Input:
		symbol (String) - The symbol of the interested instrument.
	Returns:
		(Dict) - The instrument info on Robinhood.
	'''
	def _instrument_info_by_symbol(self, symbol):
		payload = { 'symbol': symbol }
		headers = {}

		result = self._robinhood_api.query(Endpoints.BASIC_INSTRUMENT_INFO,
			payload, headers)

		# Make sure the data is there.
		if 'results' in result and len(result['results']) > 0:
			results = result['results']

			# Expect no ambiguity.
			if len(results) == 1:
				return results[0]
			else:
				raise RuntimeError("Expected only one search result when "\
					"searching for instrument info for symbol: {}.".format(
						symbol))
		else:
			raise SymbolNotFound("Not results for searching {}".format(symbol))

	'''
	Given a symbol, returns the instrument URL (typically used for placing orders).
	Input:
		symbol (String) - The symbol of the interested instrument.
	Returns:
		(String) - The instrument.
	'''
	def _instrument_url_by_symbol(self, symbol):
		return self._instrument_info_by_symbol(symbol)['url']