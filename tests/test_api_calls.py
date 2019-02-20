'''
Tests the closest to bare GET/POST requests to Robinhood API. This is the first point of notification if the Robinhood API changes from what we expect.

Unauthorized and authorized calls are separated so that simultaneous login and logout requests are not sent (login tokens are persisted through authorized call testing.)
'''

import unittest

from pyRobinhood.Endpoints import Endpoints
from pyRobinhood.Robinhood import Robinhood
from pyRobinhood.RobinhoodAPI import RobinhoodAPI
from pyRobinhood.ConfigService import ConfigService

class TestAuthorizedCalls(unittest.TestCase):

	'''
	Login and retrieval of the access token is done before testing authenticated/authorized calls.
	'''
	@classmethod
	def setUpClass(cls):
		config_service = ConfigService()
		user_info = config_service.get_user_info()

		payload = {
			'username': user_info['username'],
			'password': user_info['password'],
			'client_id': user_info['client_id'],
			'grant_type': 'password',
			'scope': 'internal'
		}
		headers = {}

		robinhood_api = RobinhoodAPI(timeout=15)
		result = robinhood_api.query(Endpoints.LOGIN, payload, headers)

		cls._access_token = result['access_token']

	def setUp(self):
		self._robinhood_api = RobinhoodAPI(timeout=15)
		self._config_service = ConfigService()

	# Test getting basic user info.
	def test_account_id(self):
		user_info = self._config_service.get_user_info()
		payload = {}
		headers = { 'Authorization': 'Bearer ' + TestAuthorizedCalls._access_token}

		result = self._robinhood_api.query(Endpoints.ACCOUNT, payload, headers)

		# Expect sensical fields from the result.
		assert('id' in result)
		assert(result['id'] != "")

class TestUnauthorizedCalls(unittest.TestCase):

	def setUp(self):
		self._robinhood_api = RobinhoodAPI(timeout=15)
		self._config_service = ConfigService()

	# Testing the getting instrument info
	def test_basic_instrument_info(self):
		payload = {
			'symbol': 'MSFT'
		}
		headers = {}

		result = self._robinhood_api.query(Endpoints.BASIC_INSTRUMENT_INFO, payload, headers)

		# Expecting the result to have a results array with length 1 (the search result).
		assert ('results' in result)
		assert(len(result['results']) == 1)

		# Expecting the search result to be sensical.
		assert('url' in result['results'][0])
		assert('list_date' in result['results'][0])
		assert(result['results'][0]['list_date'] == "1987-09-17")
		assert('country' in result['results'][0])
		assert(result['results'][0]['country'] == 'US')

	# Test getting the quote for an instrument by symbol.
	def test_quote(self):
		payload = {
			'symbol': 'MSFT'
		}
		headers = {}

		result = self._robinhood_api.query(Endpoints.QUOTE, payload, headers)

		# Expecting the result to be sensical.
		assert ('ask_price' in result)
		assert ('bid_price' in result)
		assert ('previous_close' in result)

if __name__ == '__main__':
	unittest.main()