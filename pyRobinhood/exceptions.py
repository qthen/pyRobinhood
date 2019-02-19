# Raised when logging into the Robinhood API fails.
class LoginError(Exception):
	pass

# Raised when given an unknown symbol
class SymbolNotFound(Exception):
	pass

# Raised for general API errros when querying Robinhood's private API.
# Holds the json dump of the response (if possible)
class APIError(Exception):
	def __init__(self, message, err_response = {}):

		super(APIError, self).__init__(message)

		self.err_response = response

# Raised when the user issues an authenticated method without being logged in.
class NotLoggedIn(Exception):
	pass

# Raised when an order fails (but we are unsure if it went through or not.)
class OrderFailed(Exception):
	pass

# Raised when an order is placed that may cause a day trade.
class OrderMayCauseDayTrade(Exception):
	pass