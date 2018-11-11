from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
import requests
import time
import winsound

# Replace your_api_key, your_api_secret with your api_key, api_secret
client = Client(your_api_key, your_api_secret)

#The api for prices
api = "https://api.binance.com/api/v3/ticker/price"
#The api for minimum price and minimum quantity
api1 = "https://api.binance.com//api/v1/exchangeInfo"
data = requests.get(api).json() # Retrieve data from Binance
data1 = requests.get(api1).json() # Retrieve data from Binance
data1 = data1['symbols'] # Filter data from data1

symbols = [] # The list of symbols
position = [] # The list of positions
condition = True

wait_time = 1 # Number of seconds to wait before repeating the while loop
counter = 10 # Length of the list of prices
buy_price_change = -10 # Percentage to add to current price when buying
buy_quantity_btc = 0.0022 # Quantity to buy converted from Bitcoin
expected_change_buy = 2  # Necessary change before placing a order
expected_change_sell = 25 # Expected profit
tolerance = 2 # Tolerance from max price

final_buy_price_change = 1 + buy_price_change/100 # Transform 1% to 1.01
# Filtering the data
for x in range(len(data)):
    if("BTC" in data[x]['symbol']): # Create list with cryptocurrencies that we can buy with BTC
        position.append(x)
        symbols.append(data[x]['symbol'])

price=[[] for x in range(len(position))] # Create list of lists for symbol prices
