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

# Cancels all orders for current symbol
def cancel_orders():
    id = []
    order=''
    try:
        # Retrieve open orders from Binance private Api
        order = client.get_open_orders(
            symbol=symbol, # Current symbol
            recvWindow=15000) # revWindow is maximum time difference allowed between your computer system time and Binance server time
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)

    if(order != ''): # Checks if we have received the data from the server
        for x in range(len(order)):
            id.append(order[x]['orderId']) # Creates a list of current orders

    while (id): # Cancels all orders one by one
        id1 = id[-1] # id1 will be equal with last order from list of orders
        try:    # Cancels order with Id id1
            client.cancel_order(
                symbol=symbol, # Current symbol
                orderId=id1, # Current order
                recvWindow=15000) # revWindow is maximum time difference allowed between your computer system time and Binance server time
        except BinanceAPIException as e: # If error has occurred print it
            print (e.status_code)
            print (e.message)
        id.pop(-1) # Delete last order from list because it was canceled


def sell_all(P): # Sell all quantity of current cryptocurrency at price P
    pP = P
    cancel_orders() # Cancel all orders for current symbol
    q = float(getB(symbol)) # Get total quantity available for sale for current symbol
    Qty = q - q % float(min_Qty) # Ignore quantity less than minimum quantity step

    order = ''
    try:
        order = client.order_limit_sell(
            symbol=symbol,
            recvWindow=10000, # revWindow is maximum time difference allowed between your computer system time and Binance server time
            quantity='{0:.3f}'.format(float(Qty)), # Transform string like 0.12345678910 to 0.123
            price='{0:.8f}'.format(float(pP))) # Transform string like 0.12345678910 to 0.12345678
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)

    printf(order) # Call function printf that prints order details

# Sell a specific amount of quantity ( q ) of current symbol at price p
def sell_M(p,q):
    cancel_orders() # Cancel all orders for current cryptocurrency
    pP, Qty = pQ(p,q) # Calculate correct price and quantity
    order=''
    try:
        order = client.order_limit_sell(
            symbol=symbol,
            recvWindow=15000,# revWindow is maximum time difference allowed between your computer system time and Binance server time
            quantity='{0:.8f}'.format(float(Qty)),
            price='{0:.8f}'.format(float(pP)))
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)

    printf(order) # Call function printf that prints order details

