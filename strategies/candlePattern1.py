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


def get_cadlePattern1(df, series=1):

    df['candle'] = "None"
    df['signal'] = "|--|"
    df["check"] = "No"

    for current in range(1, len(df.index)):
        if df['close'][current] >= df['open'][current]:
            df['candle'][current] = "UP"
        else:
            df['candle'][current] = "DOWN"

    PnL = 0.0

    for current in range(1, len(df.index)):
        prev = current - 1
        prev_prev = prev - 1

        if df['candle'][prev] == "UP" and df['candle'][prev_prev] == "UP":
            df['check'][current] = "Yes"

            if df['check'][prev] != "Yes":
                df['signal'][current] = "LONG"
                gain = (float(df['close'][current]) - float(df['open'][current]))
                PnL = PnL + gain

        elif df['candle'][prev] == "DOWN" and df['candle'][prev_prev] == "DOWN":
            df['check'][current] = "Yes"

            if df['check'][prev] != "Yes":
                df['signal'][current] = "SHORT"
                gain = (float(df['open'][current]) - float(df['close'][current]))
                PnL = PnL + gain

    return df, PnL

first = False
def check_buy_sell_signals(df, currency):
    global first
    current = len(df.index) - 1
    previous = current - 1
    pair = currency + "USDT"

    if first == True:
        print("(Checking for buy and sell signals)")
        if df['signal'][current] == "LONG":
            print("OPEN LONG ORDER")
            Lorder(0.007, pair, 'MARKET')
            stoploss(0.007, pair, "SELL", "LONG", stopPrice=float(df['open'][current]))
            takeprofit(0.007, pair, "SELL", "LONG", factor=0.35)
            first = False
        elif df['signal'][current] == "SHORT":
            print("OPEN SHORT ORDER")
            Sorder(0.007, pair, 'MARKET')
            stoploss(0.007, pair, "BUY", "SHORT", stopPrice=float(df['open'][current]))
            takeprofit(0.007, pair, "BUY", "SHORT", factor=0.35)
            first = False

def plot_candlePattern1(currency="ETH", timeframe='1m'):
    df = mainData(currency, timeframe)
    df = df.set_index(pd.DatetimeIndex(df['timestamp']))
    data, pnl = get_cadlePattern1(df)
    data = data.tail(50)
    #bands = mpf.make_addplot(bands)
    mc = mpf.make_marketcolors(up='#26a69a', down='#f44336', edge='black', wick={'up': '#26a69a', 'down': '#f44336'})
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle='--', facecolor='#131722')
    mpf.plot(data, type="candle", style=s)
    mpf.show()

def run_candlePattern1(serie=1, currency="ETH", timeframe='1m'):
    # Get main data
    df = mainData(currency, timeframe)

    # Calculate indicator and orders
    data, pnl = get_cadlePattern1(df, serie)
    check_buy_sell_signals(data, currency)

    # Style data to print
    #data = data.tail(5)
    drop_labels = ['high', 'low', 'volume']
    data = data.drop(drop_labels, axis=1)

    print(data)
    print(pnl)



