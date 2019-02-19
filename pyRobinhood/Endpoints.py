'''
Programmtic easy representation of Endpoints.

Should be kept in sync with RobinhoodAPI
'''

from enum import Enum

class Endpoints(Enum):
	LOGIN = 1 # Authorized
	LOGOUT = 2 # Authorized
	ORDERS = 3 # Authorized
	ACCOUNT = 4 # Unauthorized
	BASIC_INSTRUMENT_INFO = 5 # Unauthorized
	QUOTE = 6 # Unauthorized.