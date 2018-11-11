from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
from time import gmtime, strftime
from pynput import keyboard

# Replace your_api_key, your_api_secret with your api_key, api_secret
client = Client(your_api_key, your_api_secret)


data = client.get_exchange_info() # Retrieve exchange info from Binance

