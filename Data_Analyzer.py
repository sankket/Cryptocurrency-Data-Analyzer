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

# Create list neccessary for depth socked
list=[]
for x in symbols:
    list.append(x.lower()+'@depth20') # append @depth20 to each symbol and add it into list

bm = BinanceSocketManager(client)
bm.start()
depth_socket = bm.start_multiplex_socket(list,process_depth) # start depth socket
ticker_socket = bm.start_ticker_socket(process_ticker) # start price socket

# maintain candlestick lists
def kline_continuum():
    i=0
    while True:
        time.sleep(60)
        for x in range(len(symbols)):
            k_line_1m[x].pop(0)
            k_line_1m[x].append(current_price[x]) # add price to list of 1 minute candlestick every 1 minute
            if i%15==0:
                k_line_15m[x].pop(0)
                k_line_15m[x].append(current_price[x]) # add price to list of 15 minute candlestick every 15 minute
        i+=1


# Save report between ask and bit for the last 10 seconds
def report_10_seconds():
    while True:
        for x in range(len(symbols)):
            if len(ratio5_10sec[x])>10:
                ratio5_10sec[x].pop(0)
            if len(ratio5_sum_10sec[x]) > 10:
                ratio5_sum_10sec[x].pop(0)
            ratio5_10sec[x].append(ratio5[x])
            ratio5_sum_10sec[x].append(ratio5_sum[x])
        time.sleep(1)


# Calculate score for each symbol, you can add as many parameters as you want
def calculate_score():
    for x in range(len(symbols)):
            score = 0

            # 2 minute change parameter score calculation
            a = float(price_chance_2_min[x])
            if a > 0 and a < 0.5:
                score += 1
            elif a >= 0.5 and a < 1:
                score += 1.25
            elif a >= 1 and a < 1.5:
                score += 1.5
            elif a >= 1.5 and a < 2:
                score += 0.5
            elif a >= 3:
                score += 0.25

            # 5 minute change parameter score calculation
            a = float(price_chance_5_min[x])
            if a > 0 and a < 0.5:
                score += 1
            elif a >= 0.5 and a < 1:
                score += 1.25
            elif a >= 1 and a < 2:
                score += 1.5
            elif a >= 2 and a < 3:
                score += 0.5
            elif a >= 3:
                score += 0.25

            # 15 minute change parameter score calculation
            a = float(price_chance_15_min[x])
            if a <= 1 and a > -0.5:
                score += 0.25
            elif a <= -0.5 and a > -1:
                score += 0.5
            elif a <= -1 and a > -1.5:
                score += 0.75
            elif a <= -1.5:
                score += 1

            # change between 25 and 30 minutes ago parameter score calculation
            a = float(price_change_25_30_min[x])
            if a <= 2 and a > -0.75:
                score += 0.25
            elif a <= -0.75 and a > -1.25:
                score += 0.5
            elif a <= -1.25 and a > -1.75:
                score += 0.75
            elif a <= -1.75:
                score += 1

            # 1 hour change parameter score calculation
            a = float(price_chance_1_hour[x])
            if a <= 2 and a >= 0:
                score += 0.5
            elif a <= 0 and a > -2:
                score += 0.75
            elif a <= -2:
                score += 1

            # 3 hour change parameter score calculation
            a = float(price_chance_3_hour[x])
            if a <= 5 and a > -1:
                score += 0.25
            elif a <= -1 and a > -3:
                score += 0.5
            elif a <= -3 and a > -6:
                score += 0.75
            elif a <= -6:
                score += 1

            # 8 hour change parameter score calculation
            a = float(price_chance_8_hour[x])
            if a <= 0 and a > -4:
                score += 0.25
            elif a <= -4 and a > -6:
                score += 0.5
            elif a <= -6:
                score += 0.75



            if float(ratio5[x]) > 0:
                score += 1


            a = 0
            for i in range(len(ratio5_10sec[x])):
                if float(price_chance_2_min[x]) > 0.55 or float(price_chance_5_min[x]) > 1:
                    if float(ratio5_10sec[x][i]) > 0:
                        a += 1
                        if float(ratio5_sum_10sec[x][i]) > 0.3:
                            a += 1
            score += a / len(ratio5_sum_10sec[x])


            if float(ratio20[x]) > 0:
                score += 1

            a = 0
            for i in range(len(ratio5_10sec[x])-1):
                if float(ratio5_10sec[x][i]) > 0:
                    a += 1
            if a <= 2:
                score += 0.25
            elif a > 2 and a <= 4:
                score += 0.5
            elif a > 4 and a <= 7:
                score += 0.75
            elif a > 7:
                score += 1

            a = 0
            for i in range(20, 1, -1):
                if float(k_line_1m[x][-i]) > float(k_line_1m[x][-(i - 1)]):
                    a += 1
            score += a / 10

            # 1 day change parameter score calculation
            if float(price_change_1_days[x]) > 5:
                score+=0.3
            # 3 day change parameter score calculation
            if float(price_change_3_days[x]) > 10:
                score += 0.25
            # 5 day change parameter score calculation
            if float(price_change_5_days[x]) > 15:
                score += 0.25
            # 7 day change parameter score calculation
            if float(price_change_7_days[x]) > 20:
                score += 0.25
            # 10 day change parameter score calculation
            if float(price_change_10_days[x]) > -25:
                score += 0.25

            # 10 minutes moving average parameter score calculation
            a=float(average_change_10_min[x])
            if a<0.2 and a>-0.3:
                score+=0.1
            # 20 minutes moving average parameter score calculation
            a = float(average_change_20_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1
            # 50 minutes moving average parameter score calculation
            a = float(average_change_50_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1
            # 100 minutes moving average parameter score calculation
            a = float(average_change_100_min[x])
            if a < 0.2 and a > -0.3:
                score += 0.1

            # save score
            total_score[x] = score


def print_results():
    # sleep time before starting calculations
    time.sleep(10)

    while True:
        for x in range(len(symbols)):
            # calculate parameters percentages
            try:
                price_chance_2_min[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][- 2]) - 100, 2)
                price_chance_5_min[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][- 5]) - 100, 2)
                price_chance_15_min[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][- 15]) - 100, 2)
                price_chance_30_min[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][- 30]) - 100, 2)
                price_chance_1_hour[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][- 60]) - 100, 2)
                price_chance_3_hour[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][- 180]) - 100, 2)
                price_chance_8_hour[x] = round(float(current_price[x]) * 100 / float(k_line_1m[x][20]) - 100, 2)
                price_change_25_30_min[x] = round(float(k_line_1m[x][- 6]) * 100 / float(k_line_1m[x][- 30]) - 100, 2)
                price_change_1_days[x] = round(float(current_price[x]) * 100 / float(k_line_15m[x][- 96]) - 100, 1)
                price_change_3_days[x] = round(float(current_price[x]) * 100 / float(k_line_15m[x][- 288]) - 100, 1)
                price_change_5_days[x] = round(float(current_price[x]) * 100 / float(k_line_15m[x][- 480] )- 100, 1)
                price_change_7_days[x] = round(float(current_price[x]) * 100 / float(k_line_15m[x][- 672]) - 100, 1)
                price_change_10_days[x] = round(float(current_price[x]) * 100 / float(k_line_15m[x][- 960]) - 100, 1)
                average_10_min[x] = round(float(sum(k_line_1m[x][- 10:])) / 10, 8)
                average_20_min[x] = round(float(sum(k_line_1m[x][- 20:])) / 20, 8)
                average_50_min[x] = round(float(sum(k_line_1m[x][- 50:])) / 50, 8)
                average_100_min[x] = round(float(sum(k_line_1m[x][- 100:])) / 100, 8)
                average_change_10_min[x] = round(float(current_price[x]) * 100 / float(average_10_min[x]) - 100, 2)
                average_change_20_min[x] = round(float(current_price[x]) * 100 / float(average_20_min[x]) - 100, 2)
                average_change_50_min[x] = round(float(current_price[x]) * 100 / float(average_50_min[x]) - 100, 2)
                average_change_100_min[x] = round(float(current_price[x]) * 100 / float(average_100_min[x]) - 100, 2)
            except Exception as e:
                print(e)


        # call function for score calculation
        calculate_score()

        # select parameter for which data is sorted
        sort_by = total_score

        # sort data
        sorted_data = sorted(range(len(sort_by)), key=lambda k: sort_by[k])
        # sort data in reverse order
        sorted_data.reverse()

        #print table header
        print (time.ctime())
        print ('%5s %5s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %5s %6s %6s %6s %6s %6s' % (
            'Symbol', 'score', 'r5', 'r20', '2m_ch', '5m_ch', '15m_ch', '30m_ch', '1h_ch', '10MA', '20MA', '50MA', '100MA', '8h_ch',
            '25-30m',  'r5sum', '1d_ch', '3d_ch','5d_ch', '7d_ch', '10d_ch'))

        # print top 10 cryptocurrencies data
        for k in range(10):
            i = sorted_data[k]
            print ('%5s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %6s %5s %6s %6s %6s %6s %6s' % (
                symbols[i][:-3], total_score[i], ratio5[i], ratio20[i], price_chance_2_min[i], price_chance_5_min[i],
                price_chance_15_min[i],price_chance_30_min[i], price_chance_1_hour[i], average_change_10_min[i],
                average_change_20_min[i],average_change_50_min[i], average_change_100_min[i], price_chance_8_hour[i],
                price_change_25_30_min[i], ratio5_sum[i], price_change_1_days[i], price_change_3_days[i],
                price_change_5_days[i], price_change_7_days[i], price_change_10_days[i]))

        # if score for one coin is > 10 will play sound
        try:
            if float(total_score[sorted_data[0]]) > 10:
                winsound.PlaySound('\\Sound.wav', winsound.SND_FILENAME)
        except Exception as e:
            print(e)

        # Seconds to wait before repeating while loop
        time.sleep(1)



