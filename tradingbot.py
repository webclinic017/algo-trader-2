from flask import Flask, request
import alpaca_trade_api as tradeapi
import config, datetime

app = Flask(__name__)
app.debug = True

# create an instance of the rest class by calling
# the rest class from the alpaca_trade_api package/library
# and asining it to api variable
api = tradeapi.REST( config.key_id, config.secret_key, config.base_url) # or use ENV Vars shown below

#get account information and store it in the account variable.
account = api.get_account()
#api.cancel_all_orders()

api_time_format = '%Y-%m-%dT%H:%M:%S.%f-04:00'

def get_account_cash():
	account = api.get_account()
	return float(account.cash)


def get_position_qty(ticker):
	position = api.get_position(ticker)
	return position.qty

#cancells all orders
def cancel_all_orders():
	api.cancel_all_orders()

def submit_buy(ticker, close):
	account_cash = float(get_account_cash())
	quantity = int(account_cash/close)
	api.submit_order(ticker, quantity, 'buy', 'limit', 'day', limit_price=(close*1.005), stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None)

def submit_sell(ticker, close):
	cancel_all_orders()
	position = get_position_qty(ticker)
	api.submit_order(ticker, position, 'sell', 'limit', 'day', limit_price=(close*.995), stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None)

@app.route("/buy_order", methods=['POST'])
def buy_order():
	req_data = request.get_json()
	ticker =  req_data['ticker']
	exchange = req_data['exchange']
	openprice = req_data['open']
	high = req_data['high']
	low = req_data['low']
	close = req_data['close']
	volume = req_data['volume']
	time = req_data['time']
	timenow = req_data['timenow']

	submit_buy(ticker,close)

	return '''
	<h1> The ticker is {}.
		The exchange is {}.
		The open is {}.
		The high is {}.
		The low is {}.
		The close is {}.
		The volume is {}.
		The time is {}.
		The timenow is {}.
	</h1>'''.format(ticker, exchange, openprice, high, low, close, volume, time, timenow)


@app.route("/sell_order", methods=['POST'])
def sell_order():
	req_data = request.get_json()
	ticker =  req_data['ticker']
	exchange = req_data['exchange']
	openprice = req_data['open']
	high = req_data['high']
	low = req_data['low']
	close = req_data['close']
	volume = req_data['volume']
	time = req_data['time']
	timenow = req_data['timenow']

	submit_sell(ticker, close)

	return '''
	<h1> The ticker is {}.
		The exchange is {}.
		The open is {}.
		The high is {}.
		The low is {}.
		The close is {}.
		The volume is {}.
		The time is {}.
		The timenow is {}.
	</h1>'''.format(ticker, exchange, openprice, high, low, close, volume, time, timenow)

if __name__ == "__main__":
    app.run(host='0.0.0.0')


