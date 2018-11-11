from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *
import time
import threading
import winsound

# Replace your_api_key, your_api_secret with your api_key, api_secret
client = Client(your_api_key, your_api_secret)

