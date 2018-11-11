import requests
from prettytable import PrettyTable
import time
import winsound


api = "https://api.binance.com/api/v1/ticker/allPrices" # The api for prices
data = requests.get(api).json() # Calling the data from api

symbols = [] # The list of symbols
positions = [] # The list of positions

