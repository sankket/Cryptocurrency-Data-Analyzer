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


# Calculates step size for price and quantity
def calculate_min(symbol):
    for x in data1:
        if(x['symbol'] == symbol):
            min_price = float(x['filters'][0]['tickSize'])
            minQty = float(x['filters'][1]['stepSize'])
    return min_price,minQty

while (condition == True):
    data = requests.get(api).json() # Get current prices
    i = 0
    print(time.ctime()) # Print current time hh:mm:ss
    for x in position:
        if (len(price[0]) > counter): # Check if length of prices is bigger than counter
            price[i].pop(0) # Delete element from position 0
        price[i].append(data[x]['price']) # Add current price to list of prices

        if(float(price[i][0])*(1 + expected_change_buy/100) > float(data[x]['price'])): # Check if possitive change > than expected_change_buy
            # Print order details
            print("Buy: " + data[x]['symbol'] + ' at: ' + str('{0:.8f}'.format(float(data[x]['price'])
                    * final_buy_price_change)) + " from " + str(data[x]['price']))

            current_symbol= str(data[x]['symbol'])# save current symbol in current_symbol variable

            min_price,min_Qty = calculate_min(current_symbol) # Calculate minimum price and minimum quantity

            # Calculate correct price and quantity accepted by Binance server
            temp_price = float(data[x]['price']) * final_buy_price_change
            final_buy_price = temp_price - (temp_price % float(min_price))
            temp_quantity = buy_quantity_btc / float(final_buy_price)
            quantity = round((temp_quantity - ((temp_quantity % float(min_Qty)))), 8)

            order = ''
            try:
                order = client.order_limit_buy( # Place orde for buy
                    symbol=current_symbol, # Current symbol
                    recvWindow=10000, # revWindow is maximum time difference allowed between your computer system time and Binance server time
                    quantity='{0:.3f}'.format(float(quantity)), # Transform string like 0.12345678910 to 0.123
                    price='{0:.8f}'.format(float(final_buy_price))) # Transform string like 0.12345678910 to 0.12345678
            except BinanceAPIException as e: # If error has occurred print it
                print (e.status_code)
                print (e.message)


            winsound.PlaySound('\\Sound.wav', winsound.SND_FILENAME)
            condition = False
            product = x

        if(condition == False):
            break
        i=i+1
    time.sleep(wait_time)


while(True):
    try:
        status = str(order['orderId']) # save orderId in variable status
    except Exception as e: # If error has occurred print it
        print(e)
    try:
        check = client.get_order( #Check order status
            symbol= current_symbol,
            recvWindow= 10000, # revWindow is maximum time difference allowed between your computer system time and Binance server time
            orderId= status)
    except BinanceAPIException as e: # If error has occurred print it
        print (e.status_code)
        print (e.message)

    print(check['status']) # print order status
    if(check['status']== 'FILLED'): # Check if order has been filled
        print('Order Filled')
        winsound.PlaySound('\\Sound.wav', winsound.SND_FILENAME)
        break
    time.sleep(0.5)  # Wait 0.5 seconds before repeating


condition = True
max_price=0

while(condition == True):
    data = requests.get(api).json()  # Get current prices
    current_price = round(float(data[int(product)]['price']),8) # save current price in variable current_price

    if(current_price > max_price): # check if current_price > max_price
        max_price= float(current_price)

    if(current_price > float(final_buy_price)*(1 + expected_change_sell/100)
            and current_price*(1 + tolerance/100) < max_price):
        try:
            order = client.order_limit_sell( # place selling order
                symbol=current_symbol,
                recvWindow=10000,
                quantity='{0:.2f}'.format(float(quantity)),
                price='{0:.8f}'.format(float(current_price)))
        except BinanceAPIException as e:
            print (e.status_code)
            print (e.message)

        winsound.PlaySound('\\Sound.wav', winsound.SND_FILENAME)

        try:
            print(order)
        except BinanceAPIException as e:
            print(e.status_code)

        condition = False
