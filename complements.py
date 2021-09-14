import time
import ccxt
import config
import pprint
import winsound
from datetime import datetime
import pandas as pd
from binance.client import Client
import math
from _thread import *
frequency = 400  # Set Frequency To 2500 Hertz
duration = 250  # Set Duration To 1000 ms == 1 second

client = Client(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, tld='com')

exchange = ccxt.binanceusdm({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})

def getPrice(symbol):
    #symbol = symbol + "/USDT"
    bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=1)
    price = bars[0][4]
    return price

def Lorder(quantity, symbol,type='MARKET'):
    try:
        order = client.futures_create_order(
           symbol=symbol,
           side="BUY",
           positionSide="LONG",
           type=type,
           quantity=quantity,
           leverage=4
        )
        print("sending order")
        pprint.pprint(order)
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("an exception occured - {}".format(e))
        pass

def closeLorder(quantity, symbol, type='MARKET'):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side="SELL",
            positionSide="LONG",
            type=type,
            quantity=quantity,
            leverage=4
        )
        print("sending order")
        pprint.pprint(order)
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("an exception occured - {}".format(e))
        pass

def Sorder(quantity, symbol,type='MARKET'):
    try:
        print("sending order")
        order = client.futures_create_order(
            symbol=symbol,
            side="SELL",
            positionSide="SHORT",
            type=type,
            quantity=quantity,
            leverage=4
    )
        pprint.pprint(order)
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("an exception occured - {}".format(e))
        pass

def closeSorder(quantity, symbol,type='MARKET'):
    try:
        print("sending order")
        order = client.futures_create_order(
            symbol=symbol,
            side="BUY",
            positionSide="SHORT",
            type=type,
            quantity=quantity,
            leverage=4
    )
        pprint.pprint(order)
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("an exception occured - {}".format(e))
        pass

def takeprofit(quantity, pair, side, posi, factor=None, takePrice=None):
    symbol2 = pair[:-4] + "/USDT"
    take_price = 0
    if factor != None:
        if posi == "LONG":
            take_price = getPrice(symbol2) * (1 + factor / 100)
        else:
            take_price = getPrice(symbol2) * (1 - factor / 100)
    elif takePrice != None:
        take_price = takePrice

    if posi == "LONG":
        price = take_price * 1.001
    else:
        price = take_price * 0.999

    take_price = round(take_price, 2)
    price = round(price, 2)
    try:
        print("sending protection-takeprofit order")
        order = client.futures_create_order(
            symbol=pair,
            side=side,
            positionSide=posi,
            type="TAKE_PROFIT",
            price=price,
            stopPrice=take_price,
            quantity=quantity,
            leverage=4,
    )
        pprint.pprint(order)
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("an exception occured - {}".format(e))
        pass

def stoploss(quantity, pair, side, posi, factor=None, stopPrice=None):
    symbol2 = pair[:-4] + "/USDT"
    stop_price = 0
    if factor != None:
        if posi == "SHORT":
            stop_price = getPrice(symbol2) * (1 + factor / 100)
        else:
            stop_price = getPrice(symbol2) * (1 - factor / 100)
    elif stopPrice != None:
        stop_price = stopPrice

    if posi == "SHORT":
        price = stop_price * 1.001
    else:
        price = stop_price * 0.999

    stop_price = round(stop_price, 2)
    price = round(price, 2)
    try:
        print("sending protection-stoploss order")
        order = client.futures_create_order(
            symbol=pair,
            side=side,
            positionSide=posi,
            type="STOP",
            price=price,
            stopPrice=stop_price,
            quantity=quantity,
            leverage=4,
    )
        pprint.pprint(order)
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("an exception occured - {}".format(e))
        pass

def orderCheck():
    positions = []
    data = exchange.fetch_positions()
    for pos in data:
        if not pos["entryPrice"] == None:
            positions.append(pos)
    return positions

def orderCLose(id, symbol):
    exchange.cancel_order(id, symbol)

def mainData(currency="ETH", timeframe='1m', limit=150):
    # get data
    print("Fetching new " + currency + "-USDT pair " + f"bars for {datetime.now().isoformat()}")
    bars = exchange.fetch_ohlcv(str(currency) + '/USDT', timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # df, dlist = get_data(data, currency)
    return df


# HFT version
def get_data(data, currency):
    if len(data) >= 149:
        data.pop(0)
    # ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    timestamp = str(datetime.datetime.now().time())
    timestamp = timestamp[:-7]
    close = client.get_avg_price(symbol=currency + "USDT")['price']
    elements = client.get_ticker(symbol=currency + "USDT")
    list = [timestamp, round(float(elements['openPrice']), 3),
                        round(float(elements['highPrice']), 3),
                        round(float(elements['lowPrice']), 3),
                        round(float(close), 3),
                        round(float(elements['volume']), 3)]
    data.append(list)
    df = pd.DataFrame(data, columns=[currency + ': timestamp', 'open', 'high', 'low', 'close', 'volume'])
    #print(df)
    return df, data

def countdown(t, label, text):
    label.config(fg=text)
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        label.config(text=str(timer))
        t -= 1
