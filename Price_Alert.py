import requests
from prettytable import PrettyTable
import time
import winsound


api = "https://api.binance.com/api/v1/ticker/allPrices" # The api for prices
data = requests.get(api).json() # Calling the data from api

symbols = [] # The list of symbols
positions = [] # The list of positions
# Filtering the data
for x in range(len(data)):
    if('BTC' in data[x]['symbol']): # Create list with cryptocurrencies that we can buy with BTC
        positions.append(x)
        symbols.append(data[x]['symbol'])

