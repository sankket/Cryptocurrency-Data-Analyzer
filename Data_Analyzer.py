from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *
import time
import threading
import winsound

# Replace your_api_key, your_api_secret with your api_key, api_secret
client = Client(your_api_key, your_api_secret)


# Calculate list of symbols
def calculate_data_list():
    counter=0
    btc='BTC'
    symbols=[]
    all_positions=[]
    positions_final=[]
    volume=[]
    c=[]
    price_change = []
    data=client.get_ticker()
    for x in range(len(data)):
        if (btc in data[x]['symbol']) and data[x]['symbol'] != 'BTCUSDT'and data[x]['symbol'] != 'VENBTC':
            if float(data[x]['quoteVolume'])>100:
                all_positions.append(x)
    for x in all_positions:
        c.append(float(data[x]['priceChangePercent']))
    i = sorted(range(len(c)), key=lambda k: c[k])
    i.reverse()
    while (len(positions_final) < 20 and len(positions_final) < len(all_positions)):
        symbols.append(data[all_positions[i[counter]]]['symbol'])
        positions_final.append(all_positions[i[counter]])
        volume.append(data[all_positions[i[counter]]]['quoteVolume'])
        price_change.append(data[all_positions[i[counter]]]['priceChangePercent'])
        counter += 1
    return symbols, volume, positions_final, price_change


# Get candlestick data from Binance
def get_kline():
    symbols, volume, pozitii,price_change = calculate_data_list()
    prices = []
    prices1 = []
    k=[]

    for x in symbols:
        try:
            order = client.get_klines( # Get 1 minute candlestick data from server
                symbol=x,
                interval='1m')
        except BinanceAPIException as e:
            print (e.status_code)
            print (e.message)
        try:
            order1 = client.get_klines( # Get 15 minute candlestick data from server
                symbol=x,
                limit= 1000,
                interval='15m')
        except BinanceAPIException as e:
            print (e.status_code)
            print (e.message)

        if len(order1) < 970: # check if coin have at least 10 days of data
            a = symbols.index(x) # get index of x in symbols
            k.append(a)
        else:
            prices.append([]) # add empty list to list of 1 minute
            prices1.append([]) # add empty list to list of 15 minutes
            for i in range(len(order)):
                prices[-1].append(float(order[i][1])) # save 1 minute data
            for i in range(len(order1)):
                prices1[-1].append(float(order1[i][1])) # save 15 minute data
    k.reverse()

    for x in k:
        symbols.pop(x)
        volume.pop(x)
        all_positions.pop(x)
        price_change.pop(x)

    return symbols, volume, pozitii, prices, prices1,price_change
