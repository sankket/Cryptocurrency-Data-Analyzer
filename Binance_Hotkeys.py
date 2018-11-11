from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
from time import gmtime, strftime
from pynput import keyboard

# Replace your_api_key, your_api_secret with your api_key, api_secret
client = Client(your_api_key, your_api_secret)


data = client.get_exchange_info() # Retrieve exchange info from Binance
# Function to process message
def process_message(msg):
    global price_sell # declare global variable
    global price_buy # declare global variable
    price_sell = float(msg['b']) # First selling price
    price_buy = float(msg['a']) # First buying price

# Function for printing
def printf(order):
    if order != '':
        # .rstrip('0') will transform 0.14530000 to 0.1453, removes 0 from end of number
        temp_print = ('%.8f' % float(order['price'])).rstrip('0') +' ' +\
               ('%.8f' % float(order['origQty'])).rstrip('0')+\
               ' '+strftime("%X", gmtime())

        if order['side']=='BUY': # Check if order is for buying or selling, print different message for buy and sell order
            print ('B: ' + temp_print) # Print this if order is for buying
        else:
            print ('S: ' + temp_print) # Print this if order is for seling


