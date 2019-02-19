'''
First class object representation of a Quote in Robinhood.
'''

class Quote(object):

	def __init__(self, ask_price, ask_size, bid_price, bid_size,
		last_trade_price, last_extended_hours_trade_price, previous_close,
		adjusted_previous_close, previous_close_date, symbol, trading_halted,
		updated_at):
		self.ask_price = ask_price
		self.ask_size = ask_size
		self.bid_price = bid_price
		self.bid_size = bid_size
		self.last_trade_price = last_trade_price
		self.last_extended_hours_trade_price = last_extended_hours_trade_price
		self.previous_close = previous_close
		self.adjusted_previous_close = adjusted_previous_close
		self.previous_close_date = previous_close_date
		self.symbol = symbol
		self.trading_halted = trading_halted
		self.updated_at = updated_at