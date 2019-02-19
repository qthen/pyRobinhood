'''
Instance that can query the Robinhood API. Understands what endpoints are authorized (and which are not). 
'''

import requests

from pyRobinhood.exceptions import APIError
from pyRobinhood.Endpoints import Endpoints

class RobinhoodAPI(object):

	# Should be kept in sync with Endpoints
	UNAUTHORIZED_ENDPOINTS = set([Endpoints.LOGIN, Endpoints.BASIC_INSTRUMENT_INFO, Endpoints.QUOTE])
	AUTHORIZED_ENDPOINTS = set([Endpoints.ACCOUNT, Endpoints.LOGOUT, Endpoints.ORDERS])
	ENDPOINTS_MAP = {
		Endpoints.LOGIN: "https://api.robinhood.com/oauth2/token/",
		Endpoints.LOGOUT: "https://api.robinhood.com/oauth2/revoke_token/",
		Endpoints.ACCOUNT: "https://api.robinhood.com/accounts/",
		Endpoints.BASIC_INSTRUMENT_INFO: "https://api.robinhood.com/instruments/",
		Endpoints.ORDERS: "https://api.robinhood.com/orders/",
		Endpoints.QUOTE: "https://api.robinhood.com/quotes/"
	}
	
	'''
	Inputs:
		timeout (Int) - How long each request should take before timing out.
	'''
	def __init__(self, timeout):
		self.TIMEOUT = timeout

	'''
	Queries the given endpoint with request and returns the response as a JSON
	'''
	def query(self, endpoint, payload, headers):

		# Make sure the endpoint is the type we expect.
		if not isinstance(endpoint, Endpoints):
			raise TypeError("Expected endpoint to be of Enum type Endpoints.")

		# If the endpoint is authorized, expect an Authorization header.
		if endpoint in RobinhoodAPI.AUTHORIZED_ENDPOINTS and 'Authorization' not in headers:
			raise ValueError("Endpoint: {} is authorized but no Authorization header was specified.".format(endpoint))

		# Make sure URI path is available.
		if endpoint not in RobinhoodAPI.ENDPOINTS_MAP:
			raise RuntimeError("Endpoint {} not in ENDPOINTS_MAP constant, this suggest code is out of sync with each other.".format(endpoint))
		
		# Query the URI.
		uri_path = RobinhoodAPI.ENDPOINTS_MAP[endpoint]

		if endpoint is Endpoints.LOGIN or endpoint is Endpoints.ORDERS: # POST requests.
			r = requests.post(uri_path, data=payload, headers=headers, timeout=self.TIMEOUT)
		elif endpoint is Endpoints.ACCOUNT or endpoint is Endpoints.BASIC_INSTRUMENT_INFO: # GET requests.
			r = requests.get(uri_path, params=payload, headers=headers, timeout=self.TIMEOUT)
		elif endpoint is Endpoints.QUOTE:
			if 'symbol' in payload:
				# Request through url parameter.
				uri_path += payload['symbol']
				r = requests.get(uri_path, headers=headers, timeout=self.TIMEOUT)
			else:
				raise ValueError("'symbol' must be provided in payload for endpoint: {}".format(endpoint))
		else: # Unrecognized endpoint.
			raise ValueError("Given unknown endpoint to query: {}".format(endpoint))

		# Raise APIError if status code is not 200
		if r.status_code == 200 || r.status_code == 201:
			return r.json()
		else:
			raise APIError("Querying endpoint {} returned non-200 HTTP status code".format(endpoint), r.json())