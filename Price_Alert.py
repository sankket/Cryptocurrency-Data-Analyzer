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

# Creating the table
table = PrettyTable()
table.field_names = ["Symbol","Change"] # Declare table headers


wait_time = 1 # Number of seconds to wait before repeating the while loop
counter = 12 # Length of the list of prices
up_change = 0.75 # Minimum up change necessary for inserting it inside the table
down_change = -0.75 # Minimum down change necessary for inserting it inside the table
alert_change = 1.5 # Minimum change necessary for alerting user with sound


prices = [[] for y in range(len(symbols))] # Create list of lists for symbol prices

while(True):
    has_rows = False
    play_alert = False
    data = requests.get(api).json() # Get current prices

    i = 0
    for x in positions:
        if (len(prices[i]) > counter): # Check if length of prices is bigger than counter
            prices[i].pop(0) # Delete element from position 0
        prices[i].append(data[x]['price']) # Add current price to list of prices

        if((float(prices[i][-1]) > float(prices[i][0]) * (1 + up_change / 100) or # Check if possitive change > than up_change
                float(prices[i][-1]) < float(prices[i][0]) * (1 + down_change / 100))): # Check if  negative change > than down_change
            current_symbol = symbols[i] # save current symbol in current_symbol variable
            current_price = round(float(prices[i][-1]) * 100 / float(prices[i][0]) - 100, 2) # save current price change in current_price variable
            table.add_row([ current_symbol, current_price]) # Add symbol and price to table
            has_rows = True
            if(current_price > alert_change):
                play_alert = True
        i += 1

    if ( has_rows == True): # Check if table has rows
        table.sortby = "Change" # sort table by change
        table.reversesort = True # Set reversesort to true

        print(" ")
        print("---- " + time.strftime('%X') + " ----") # Print current time hh:mm:ss
        print(table)

    if( play_alert == True): # If change is > alert_change play sound
        winsound.PlaySound('\\Sound.wav', # '\\name of file.wav' has to be in folder where this file is if you use just \\
                           winsound.SND_FILENAME)
    table.clear_rows() # Refresh table
    time.sleep(wait_time) # Wait wait_time seconds before repeating
