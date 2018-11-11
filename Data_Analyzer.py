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

