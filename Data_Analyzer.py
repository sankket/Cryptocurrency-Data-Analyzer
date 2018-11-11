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
# Calculate report between bid and ask offers
def process_depth(msg):
    sums5=0
    sumb5=0
    m=-1
    for x in range(5):
        if float(msg['data']['bids'][x][1])>m:
            m=float(msg['data']['bids'][x][1])
        sums5 = sums5 + float(msg['data']['bids'][x][1])
        sumb5 = sumb5 + float(msg['data']['asks'][x][1])
    ratio1 = sums5 / sumb5
    if (ratio1 < 1):
        ratio1 = ((1 / ratio1) * -1) + 1
    else:
        ratio1 -= 1
    sums20 = 0
    sumb20 = 0
    ratio2 = 0
    try:
        for x in range(17):
            sums20 = sums20 + float(msg['data']['bids'][x][1])
            sumb20 = sumb20 + float(msg['data']['asks'][x][1])
        ratio2 = sums20 / sumb20
        if (ratio2 < 1):
            ratio2 = ((1 / ratio2) * -1) + 1
        else:
            ratio2 -= 1
    except Exception as e:
        print("")

    for i in range(len(symbols)):
        simbol = symbols[i].lower() + '@depth20'
        if simbol == msg['stream']:
            ratio5[i] = round(ratio1, 2)
            ratio20[i] = round(ratio2, 2)
            max_order5[i] = m
            ratio5_sum[i] = round(float(sums5) * float(current_price[i]) * 100 / float(volume[i]),2)
            current_price[i] = float(msg['data']['bids'][0][0])


# Refresh price and volume to current price and volume
def process_ticker(msg):
    i=0
    for x in symbols:
        for y in range(len(msg)):
            if x == str(msg[y]['s']):
                volume[i] = int(float(msg[y]['q']))
                price_change[i] = int(float(msg[y]['P']))
        i+=1

symbols,volume,pozitii,k_line_1m,k_line_15m,price_change =get_kline()


# Declaring lists necessary for storing data
max_order5=[0 for x in range(len(symbols))]
current_price= [0 for x in range(len(symbols))]
price_chance_2_min = [0 for x in range(len(symbols))]
price_chance_5_min = [0 for x in range(len(symbols))]
price_chance_15_min = [0 for x in range(len(symbols))]
price_chance_30_min = [0 for x in range(len(symbols))]
price_change_25_30_min = [0 for x in range(len(symbols))]
price_chance_1_hour = [0 for x in range(len(symbols))]
price_chance_3_hour = [0 for x in range(len(symbols))]
price_chance_8_hour = [0 for x in range(len(symbols))]
price_change_1_days = [0 for x in range(len(symbols))]
price_change_3_days = [0 for x in range(len(symbols))]
price_change_5_days = [0 for x in range(len(symbols))]
price_change_7_days = [0 for x in range(len(symbols))]
price_change_10_days = [0 for x in range(len(symbols))]
average_10_min = [0 for x in range(len(symbols))]
average_20_min = [0 for x in range(len(symbols))]
average_50_min = [0 for x in range(len(symbols))]
average_100_min = [0 for x in range(len(symbols))]
average_change_10_min = [0 for x in range(len(symbols))]
average_change_20_min = [0 for x in range(len(symbols))]
average_change_50_min = [0 for x in range(len(symbols))]
average_change_100_min = [0 for x in range(len(symbols))]
total_score = [0 for x in range(len(symbols))]
ratio5=[0 for x in range(len(symbols))]
ratio5_10sec=[[] for y in range(len(symbols))]
ratio5_sum = [0 for x in range(len(symbols))]
ratio5_sum_10sec = [[] for y in range(len(symbols))]
ratio20= [0 for x in range(len(symbols))]

