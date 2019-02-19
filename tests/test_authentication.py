'''
The tests for authentication are separated from the other api call tests because we want the access token to persist for authenticated calls, thus the actual testing for login/logout is done here.
'''

import unittest

from pyRobinhood.Endpoints import Endpoints
from pyRobinhood.Robinhood import Robinhood
from pyRobinhood.RobinhoodAPI import RobinhoodAPI
from pyRobinhood.ConfigService import ConfigService

class TestAuthentication(unittest.TestCase):

	def setUp(self):
		self._robinhood_api = RobinhoodAPI(timeout=15)
		self._config_service = ConfigService()

	# Testing the login call.
	def test_login(self):
		user_info = self._config_service.get_user_info()

		payload = {
			'username': user_info['username'],
			'password': user_info['password'],
			'client_id': user_info['client_id'],
			'grant_type': 'password',
			'scope': 'internal'
		}
		headers = {}

		result = self._robinhood_api.query(Endpoints.LOGIN, payload, headers)

		# Expecting the token to be populated in the access_token property
		assert('access_token' in result)
		assert(result['access_token'] != "")

if __name__ == '__main__':
	unittest.main()