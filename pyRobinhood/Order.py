'''
A first class object representation of an order on Robinhood.
'''

class Order(object):

	'''
	Arguments are identical to response field of a sent order.
	Inputs:
		id (String) - The order id.
		fees (Float) - Total fees.
		cancel (String) - POST URL to cancel order.
		cumulative_quantity (Float) - Number of shares executed so far.
		reject_reason (String) - If the order was rejected, the reason.
		url (String) - URL with up to date information.
		updated_at (ISO 8601) - Last updated at.
		created_at (ISO 8601) - Time the order was placed at.
		average_price (Float) - Average price of all shares executed so far.
	'''
	def __init__(self, id, fees, cancel, cumulative_quantity, reject_reason,
		state, url, updated_at, created_at, average_price):
		self.id = id
		self.fees = fees
		self.cancel = cancel
		self.cumulative_quantity = cumulative_quantity
		self.reject_reason = reject_reason
		self.state = state
		self.url = url
		self.updated_at = updated_at
		self.created_at = created_at
		self.average_price = average_price