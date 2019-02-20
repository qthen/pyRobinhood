# pyRobinhood

Python framework for interacting with Robinhood's API.

## Supports

1. Market BUY/SELL orders.
2. LIMIT BUY/SELL orders.
3. Stock quotes.

## Upcoming

1. Stop loss orders.
2. Accounts with two-factor authentication enabled.

## Usage

pyRobinhood exposes trading orders in the same way they are presented in Robinhood front end. `Robinhood` exposes these through `place_market_buy`, `place_market_sell`, `place_limit_buy`, and `place_limit_sell`. First, a login request must be successfully made before any trades can be done. Below is a simple login with buy/sell orders being made. 

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