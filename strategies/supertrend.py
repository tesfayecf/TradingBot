import ccxt
import config
import warnings
import pandas as pd
import mplfinance as mpf
from datetime import datetime
from complements import mainData, Lorder, closeLorder, Sorder, closeSorder, stoploss, takeprofit
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 15)
pd.set_option("display.precision", 8)


# tancar posicio quan el pnl arriba a x o hi ha un alerta per obrir una posicio contraria
# fer servir _thread per alhora buscar noves entrades i mirar el pnl

exchange = ccxt.binanceusdm({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})

def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr

def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr

def get_supertrend(df, period, atr_multiplier):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = round(hl2 + (atr_multiplier * df['atr']), 3)
    df['atr_upperband'] = round(hl2 + (atr_multiplier * df['atr']), 3)
    df['lowerband'] = round(hl2 - (atr_multiplier * df['atr']), 3)
    df['atr_lowerband'] = round(hl2 - (atr_multiplier * df['atr']), 3)
    df['trend'] = "UP"

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['trend'][current] = "UP"
            #df['upperband'] = 0

        elif df['close'][current] < df['lowerband'][previous]:
            df['trend'][current] = "DOWN"
            #df['lowerband'] = 0
        else:
            df['trend'][current] = df['trend'][previous]

            if df['trend'][current] == "UP" and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if df['trend'][current] == "DOWN" and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df

first = True
def check_buy_sell_signals(df, currency):
    global first
    print("(Checking for buy and sell signals)")
    #print(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    pair = currency + "USDT"

    if first == True:
        if df['trend'][last_row_index] == "UP":
            print("OPEN LONG ORDER")
            #Lorder(0.007, pair, 'MARKET')
            first = False
        elif df['trend'][last_row_index] == "DOWN":
            print("OPEN SHORT ORDER")
            #Sorder(0.007, pair, 'MARKET')
            first = False
    else:
        if df['trend'][previous_row_index] == "DOWN" and df['trend'][last_row_index] == "UP":
            print("CHANGED TO UPTREND, BUY")
            try:
                print("CLOSE SHORT ORDER PREVIOUSLY OPENED")
                #closeSorder(0.007, pair, 'MARKET')
            except:
                pass
            print("OPEN LONG ORDER")
            #Lorder(0.007, currency, 'MARKET')
        if df['trend'][previous_row_index] == "UP" and df['trend'][last_row_index] == "DOWN":
            print("CHANGED TO DOWNTREND, SELL")
            try:
                print("CLOSE LONG ORDER PREVIOUSLY OPENED")
                #closeLorder(0.007,pair,'MARKET')
            except:
                pass
            print("OPEN SHORT ORDER")
            #Sorder(0.007, pair, 'MARKET')

            #takeprofit(0.015, currency, "BUY", "SHORT", profit)
            #stoploss(0.013, currency, "BUY", 0.99)
        else:
            print("NO MOVEMENT")

def plot_supetrend(period, atr_multiplier,currency="ETH", timeframe='1m'):
    df = mainData(currency, timeframe)
    df = df.set_index(pd.DatetimeIndex(df['timestamp']))
    data = get_supertrend(df, period, atr_multiplier)
    data = data.tail(int(period))
    drop_labels = ['timestamp', 'close', 'open', 'low', 'high', 'volume', 'previous_close', 'high-low', 'high-pc',
                    'low-pc', 'tr', 'atr', 'trend']
    bands = data.drop(drop_labels, axis=1)
    print(bands)
    #bands = mpf.make_addplot(bands)
    band_plot = [
        mpf.make_addplot(bands['lowerband'], color='#008000'),
        mpf.make_addplot(bands['upperband'], color='#ff0000'),
        mpf.make_addplot(bands['atr_upperband'], color='#3bb3e4'),
        mpf.make_addplot(bands['atr_lowerband'], color='#3bb3e4')]
    mc = mpf.make_marketcolors(up='#26a69a', down='#f44336', edge='black', wick={'up': '#26a69a', 'down': '#f44336'})
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle='--', facecolor='#131722')
    mpf.plot(data, type="candle", style=s, addplot=band_plot)
    mpf.show()


def run_superTrend(period, atr_multiplier,currency="ETH", timeframe='1m'):
    # Get main data
    df = mainData(currency, timeframe)

    # Calculate indicator and orders
    supertrend_data = get_supertrend(df, period, atr_multiplier)
    check_buy_sell_signals(supertrend_data, currency)

    # Style data to print
    supertrend_data = supertrend_data.tail(5)
    drop_labels = ['open', 'high', 'low', 'previous_close', 'high-low', 'high-pc', 'low-pc', 'tr', 'atr', 'atr_upperband', 'atr_lowerband']
    data = supertrend_data.drop(drop_labels, axis=1)
    #data = tabulate(data, headers='keys', tablefmt='plain')

    print(data)

    return data

