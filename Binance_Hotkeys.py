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

# Calculates correct price and quantity
# p, pP is price and q, Qty is quantity, bal is quantity available from current symbol
def pQ(p,q):
    p=float(p)
    q=float(q)
    pP = p - p % min_price
    if q == 0: # If quantity is not specified will sell all available quantity
        if symbol == 'BTCUSDT':
            bal = float(getB('USDT'))
            Qty = bal / p - bal / p % min_Qty
        else:
            q = float(getB(symbol))
            Qty = q - q % min_Qty
    elif symbol == 'BTCUSDT':
        Qty = q - q % min_Qty
    else:
        Qty = q / pP - q / pP % min_Qty
    return pP , Qty

# Buy a specific amount of quantity ( q ) of current symbol at price p
def buy_M(p,q):
    cancel_orders() # Cancel all orders for current symbol
    pP,Qty= pQ(p,q) # Calculate correct price and quantity
    order = ''
    try:
        order = client.order_limit_buy(
            symbol=symbol,
            recvWindow=10000, # revWindow is maximum time difference allowed between your computer system time and Binance server time
            quantity='{0:.8f}'.format(float(Qty)),
            price='{0:.8f}'.format(float(pP)))
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)

    printf(order) # Call function printf that prints order details


# Calculates asset,asset is necessary for placing a get_asset_balance order
def calc_asset(symbol):
    if symbol == "BTCUSDT":
        asset=symbol[:-4] # asset will be equal to symbol - last 4 characters (last 4 characters being USDT)
    elif symbol == "USDT":
        asset="USDT"
    else:
        asset = symbol[:-3] # asset will be equal to symbol - last 3 characters (last 3 characters being BTC)
    return asset

# Get balance for specified symbol
def getB(symbol):
    asset = calc_asset(symbol) # Calculate asset, asset is necessary for placing a get_asset_balance order
    order=''
    try:
        order = client.get_asset_balance(
            asset= asset, # Current asset
            recvWindow=10000) # revWindow is maximum time difference allowed between your computer system time and Binance server time
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)
    if order != '':
        if float(order['free']) > 0: # Check if current available quantity is greater than 0
            return order['free']
        else:
            print("0 Balance gB")
            return min_Qty


# Just another function for selling
def sell_F(pP,quantity):
    if symbol == 'BTCUSDT':
        sell_M(pP, quantity)
    else:
        sell_all(pP)

def on_pres(key):
    while 'price_sell' not in globals(): # Wait until we receive the prices from server
        cc = '' # Garbage

    # Calculate pressed key
    try:
        k = key.char
    except:
        k = key.name

    if key == keyboard.Key.esc:
        return False

    pS = float(price_sell) + min_price # First available ask price + 1 price step
    pS1 = float(price_sell) - min_price # First available ask price - 1 price step
    pL = float(price_buy) - min_price # First available bit price - 1 price step


    # Show average buying price for current quantity available for current symbol
    if k in ['a']:
        bal = float(getB(symbol))
        p,q=trades(bal)
        print ('AvP: '+str('%.8f' % (float(p)-float(p)%float(min_price))).rstrip('0')
               .rstrip('.')+" Q: "+str(bal))

    if k in ['up']:
        if symbol =="BTCUSDT":
            buy_M(pS1,0)
        else:
            buy_M(price_sell * 0.999,quantity)

    if k in ['right']: buy_M(pS,quantity)

    if k in ['down']: sell_F(pL, quantity)

    if k in ['0']: buy_M(pS + min_price, quantity)

    # Place order for buy at 90% of current ask price
    if k in ['1']: buy_M(price_sell*0.90, quantity)

    # Place order for buy at 80% of current ask price
    if k in ['2']: buy_M(price_sell * 0.8, quantity)

    if k in ['left']: sell_F(pS1,quantity)

    # Place buy order for equivalent of 0.002 bitcoin at current ask price + 1 price step
    if k in ['e']: buy_M(pS, 0.002)

    # Place buy order for equivalent of 0.003 bitcoin at current ask price + 1 price step
    if k in ['d']: buy_M(pS, 0.002)

    # Place sell order for equivalent of 0.01 bitcoin at current bit price - 1 price step
    if k in ['w']: sell_M(pL, 0.01)

    # Place sell order for equivalent of 0.02 bitcoin at current bit price - 1 price step
    if k in ['s']: sell_M(pL, 0.02)

    # Sell available quantity at average buying price + 0.5%
    if k in ['z']: if_average(1.005)

    # Sell available quantity at average buying price + 0.8%
    if k in ['x']: if_average(1.008)

    # Sell available quantity at average buying price + 1%
    if k in ['c']: if_average(1.01)

    # Pause
    if k in ['p']:
        return False

    # Calcel all orders for current symbol
    if k in ['q']:
        print ("Canceled")
        cancel_orders()

# Sell at average price * a, of average price is available
def if_average(a):
    b=1.9999-a
    cancel_orders()
    if symbol == "BTCUSDT":
        bal = float(getB("USDT"))
        if ( bal / price_sell) > 0.002:
            p , q = trades(bal)
            p = p * b
            q = q * a
            buy_M(p,q)
        elif (bal / price_sell) > 0.001:
            print ('Low Balance')
    else:
        bal = float(getB(symbol))
        if bal * price_buy > 0.002:
            p, q = trades(bal)
            p = p * a
            sell_M(p,q)
        elif bal * price_buy > 0.001:
            print('Low Balance')

def trades(bal):
    order=''
    # Retrieve data for last 40 trades
    try:
        order = client.get_my_trades(
                    symbol=symbol,
                    limit=40,
                    recvWindow=15000)
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)

    i=len(order)-1
    averagePrice = tVal = tQty = 0 # tVal = total value, tQty = total quantity
    if order != '': # Checks if we have received the data from the server
        if (symbol == "BTCUSDT"): # Check if current symbol is BTCUSDT
            while i > -1 and tVal < bal: # Go  through last 40 orders and calculate average buying price for current symbol
                if str(order[i]['isBuyer']) == 'False':
                    if ( tVal + float(order[i]['price']) * float(order[i]['qty']) > bal):
                        tQty = tQty + ( bal - tVal ) / float(order[i]['price'])
                        tVal = bal
                    else:
                        tVal = tVal + float(order[i]['price']) * float(order[i]['qty'])
                        tQty = tQty + float(order[i]['qty'])
                i = i - 1
            averagePrice = bal / tQty
            tQty = bal / averagePrice
        else:
            while i > -1 and tQty < bal: # Go  through last 40 orders and calculate average buying price for current symbol
                if str(order[i]['isBuyer']) == 'True':
                    if (tQty + float(order[i]['qty']) > bal):
                        tVal = tVal + float(order[i]['price'])*( bal - tQty)
                        tQty = tQty + (bal - tQty)
                    else:
                        tVal = tVal + float(order[i]['price']) * float(order[i]['qty'])
                        tQty = tQty + float(order[i]['qty'])
                i = i - 1
            averagePrice = tVal / tQty
            tQty= averagePrice * bal
    else:
        print ("Error Average Price for Trades")
    return averagePrice,tQty

# quantity has to be > 0.002 because minimum trading quantity on Binance is 0.002
quantity=0.0021

while True:
    h = raw_input('Pres enter')
    s = raw_input('symbol: ')
    s = s.upper()

    if s == 'BTC':
        symbol = s + "USDT"
    else:
        symbol = s + "BTC"

    bm = BinanceSocketManager(client)
    conn_key = bm.start_symbol_ticker_socket(symbol, process_message) # Connect to price socket from Binance
    bm.start() # Start connection to price socket from Binance

    # Calculate step size for price and quantity
    for x in range(len(data['symbols'])):
        if (symbol in data['symbols'][x]['symbol']):
            min_price = float(data['symbols'][x]['filters'][0]['tickSize']) # minimum price step
            min_Qty = float(data['symbols'][x]['filters'][1]['stepSize']) # minimum quantity step

    # Start listening to your key presses
    lis = keyboard.Listener(on_press=on_pres)
    lis.start()
    lis.join()
    bm.close()
