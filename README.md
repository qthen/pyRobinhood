# pyRobinhood

Python framework to interact with Robinhood's API presented in front end style.

## Supports

1. Market buy/sell, limit buy/sell
2. Quotes

## Does not support

1. Accounts with two-factor authentication enabled.

## Usage

pyRobinhood exposes trading orders in the same way they are presented in Robinhood front end. 

```
from pyRobinhood.Robinhood import Robinhood
robinhood = Robinhood()
if (robinhood.login("myemail@email.com", "mypassword")) {
	# Login successful, place orders.

	# Market BUY order.
	robinhood.place_market_buy(symbol = 'FB', quantity = 100)

	# Market SELL order.
	robinhood.place_market_sell(symbol = 'AMZN', quantity = 100)

	# LIMIT BUY order.
	robinhood.place_limit_buy(symbol = 'AAPL', quantity = 100, price = 100.00)

	# LIMIT SELL order.
	robinhood.place_limit_sell(symbol = 'GOOG', quantity = 100, price = 1000.00)
}
```