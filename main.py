from binance.client import Client
import time
from decimal import Decimal as D
from credentials import credential

api_key, api_secret = credential() 

client = Client(api_key, api_secret)
old_ticker_list = []
start = time.time()
asset = "ADAUSDT"

all_asset_ticker = client.get_all_tickers()

symbol_info = client.get_symbol_info(asset)
price_filter = float(symbol_info['filters'][0]['tickSize'])
minimum = float(symbol_info['filters'][2]['minQty'])
ticker = client.get_symbol_ticker(symbol="{}".format(asset))
price = float(ticker["price"])
quantity = 11/price

def buy_quantity():
    price = float(ticker["price"])
    quantity = 11/price
    buying_quantiity = D.from_float(quantity).quantize(D(str(minimum)))
    return buying_quantiity


def get_coins():
    for i in range(len(all_asset_ticker)):
        symbols = all_asset_ticker[i]["symbol"]
        old_ticker_list.append(symbols)
get_coins()


def refreshed_all_coins():
    refreshed_ticker_list = []
    for i in range(len(all_asset_ticker)):
        symbols = all_asset_ticker[i]["symbol"]
        refreshed_ticker_list.append(symbols)
    return refreshed_ticker_list

end = time.time()

def non_match_elements(list_a, list_b):
    non_match = []
    for i in list_a:
        if i not in list_b:
            non_match.append(i)
    return non_match


refreshed_ticker = refreshed_all_coins()

i=1
while i !=5:
    non_match = non_match_elements(old_ticker_list, refreshed_ticker)
    if non_match == []:
        print("No Match")
        i+=1
        continue
    else:
        print("mached")
        order = client.order_market_buy(
            symbol=asset,
            quantity=buy_quantity())
        print("Bought For: {}".format(price))

        order = client.order_market_sell(
            symbol=asset,
            quantity=buy_quantity(),)
        print("Sold For: {}".format(price))

        break




print("Time Taken:",end-start)
print(buy_quantity())