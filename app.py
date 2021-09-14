import time
import ccxt
import config
import tkinter as tk
from _thread import *
from tkinter import ttk
import tkinter.font as font
from strategies.supertrend import run_superTrend, plot_supetrend
from strategies.candlePattern1 import run_candlePattern1, plot_candlePattern1
from tkinter_custom_button import TkinterCustomButton
from complements import countdown, orderCheck, getPrice

#"#9bd1b4"
background = "#1b2218"
blackColor = '#000000'
entryBackground = '#a99701'
hoverColor = "#705901"
hoverColor2 = "#705901"
text = "#c5c5bd"
timetext = '#a99701'
positive = "#036800"
negative = "#d52524"

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

exchange = ccxt.binanceusdm({
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})

root = tk.Tk()

canvas = tk.Canvas(root, height=720, width=1200, bg=text)
canvas.pack()

image = tk.PhotoImage(file='crypto_image3.png')
canvas.create_image(600, 360, image=image)

frame = tk.Frame(canvas, bg=background)
frame.place(relheight=0.85, relwidth=0.85, relx=0.075, rely=0.075)

labelFont = font.Font(size=15)
labelFont1 = font.Font(size=14)
labelFont2 = font.Font(size=12)
myFont0 = font.Font(size=35, family='System')

label0 = tk.Label(frame, text="TRADING BOT", bg=background, fg=text)
label0['font'] = myFont0
label0.pack()
label0.place(relx=0.35, rely=0.1)

multiplier = tk.Entry(frame, width=5, bg=entryBackground, fg=blackColor)
multiplier['font'] = labelFont
multiplier.pack()
multiplier.place(relx=0.15, rely=0.10)
label1 = tk.Label(frame, text="Multiplier", bg=background, fg=text)
label1['font'] = labelFont
label1.pack()
label1.place(relx=0.05, rely=0.1)

period = tk.Entry(frame, width=5, bg=entryBackground, fg=blackColor)
period['font'] = labelFont
period.pack()
period.place(relx=0.15, rely=0.15)
label2 = tk.Label(frame, text="Period", bg=background, fg=text)
label2['font'] = labelFont
label2.pack()
label2.place(relx=0.05, rely=0.15)


currency = tk.StringVar()
def assignCurrency(value):
    global currency
    currency = value

dropc = tk.OptionMenu(frame, currency, "BTC", "ETH", "BNB", "LINK", "ADA", "DOT", command=assignCurrency)
dropc.config(bg=background, fg=text)
dropc["menu"].config(bg=background, fg=text)
dropc.pack()
dropc.place(relx=0.90, rely=0.11)
label3 = tk.Label(frame, text="Currency", bg=background, fg=text)
label3['font'] = labelFont
label3.pack()
label3.place(relx=0.8, rely=0.11)

timeframe = tk.StringVar()
def assignTimeframe(value):
    global timeframe
    timeframe = value

dropt = tk.OptionMenu(frame, timeframe, "1m", "5m", "15m", "30m", "1h", "2h", "5h", command=assignTimeframe)
dropt.config(bg=background, fg=text)
dropt["menu"].config(bg=background, fg=text)
dropt.pack()
dropt.place(relx=0.90, rely=0.16)
label4 = tk.Label(frame, text="Timeframe", bg=background, fg=text)
label4['font'] = labelFont
label4.pack()
label4.place(relx=0.8, rely=0.16)

# Pnl labels
label5 = tk.Label(frame, text="PnL: ", bg=background, fg=background)
label5['font'] = labelFont2
label5.pack()
label5.place(relx=0.07, rely=0.70)

label6 = tk.Label(frame, text="PnL: ", bg=background, fg=background)
label6['font'] = labelFont2
label6.pack()
label6.place(relx=0.07, rely=0.75)

label7 = tk.Label(frame, text="PnL: ", bg=background, fg=background)
label7['font'] = labelFont2
label7.pack()
label7.place(relx=0.07, rely=0.8)

label8 = tk.Label(frame, text="PnL: ", bg=background, fg=background)
label8['font'] = labelFont2
label8.pack()
label8.place(relx=0.07, rely=0.85)


label11 = TkinterCustomButton(master=frame,
                              text="UPDATE",
                              width=80,
                              height=30,
                              bg_color=background,
                              hover_color=hoverColor2,
                              fg_color=background,
                              text_color=timetext,
                              command=lambda: threadUpdateOne(period.get(), multiplier.get(), currency, timeframe))

#label11['font'] = labelFont2
#label11.pack()
label11.place(relx=0.88, rely=0.87)

label12 = tk.Label(frame, width=20, text="00:00", bg=background, fg=timetext)
label12['font'] = labelFont2
label12.pack()
label12.place(relx=0.83, rely=0.92)

label13 = TkinterCustomButton(master=frame,
                              text="PLOT",
                              width=80,
                              height=30,
                              corner_radius=150,
                              bg_color=background,
                              hover_color=hoverColor2,
                              fg_color=background,
                              text_color=timetext,
                              command=lambda: threadPlot(period.get(), multiplier.get(), currency, timeframe))
label13.place(relx=0.03, rely=0.91)

def threadPlot(period=period.get(), multiplier=multiplier.get(), currency=currency, timeframe=timeframe):
    start_new_thread(plot_supetrend, (int(period), int(multiplier), currency, timeframe))

def dataWrite(data, frame=frame):
    myFont = font.Font(size=15)
    global label
    label = tk.Label(frame, text=data, bg=background, fg=text)
    label['font'] = myFont
    label.pack()
    label.place(relx=0.15, rely=0.40)

def dataUpdate(data):
    label.config(text=data)

def pnlWrite(pos, label):
    pnl = round(pos['unrealizedPnl'], 4)
    side = pos['side']
    entryPrice = pos['entryPrice']
    symbol = pos['symbol']
    actualPrice = getPrice(symbol)
    liquidationPrice = pos['liquidationPrice']
    notional = round(pos['notional'],3)

    label.config(text="PnL: " + str(pnl) + "  Price: " + str(actualPrice) + "  EntryPrice: " + str(
        entryPrice) + "  Asset: " + symbol +
          "  Size: " + str(notional) + "USD" + "  Side: " + side + "  LiquidationPrice: " + str(
        liquidationPrice))
    if pnl == 0:
        label.config(fg=text, bg=background)
    elif pnl > 0:
        label.config(fg=text, bg=positive)
    else:
        label.config(fg=text, bg=negative)

def pnlUpdate(positions):

    x = 1
    length = len(positions)

    if length == 0:
        label5.config(fg=background, bg=background)
        label6.config(fg=background, bg=background)
        label7.config(fg=background, bg=background)
        label8.config(fg=background, bg=background)
    elif length == 1:
        label6.config(fg=background, bg=background)
        label7.config(fg=background, bg=background)
        label8.config(fg=background, bg=background)
    elif length == 2:
        label7.config(fg=background, bg=background)
        label8.config(fg=background, bg=background)
    elif length == 3:
        label8.config(fg=background, bg=background)
    else:
        pass

    for pos in positions:

            if x == 1:
                pnlWrite(pos, label5)
            elif x == 2:
                pnlWrite(pos, label6)
            elif x == 3 :
                pnlWrite(pos, label7)
            elif x == 4:
                pnlWrite(pos, label8)
            else:
                pass
            x = x + 1

def updateOne(period=period.get(), multiplier=multiplier.get(), currency=currency, timeframe=timeframe):
    data = run_superTrend(int(period), int(multiplier), currency, timeframe)
    dataWrite(data)

def threadUpdateOne(period=period.get(), multiplier=multiplier.get(), currency=currency, timeframe=timeframe):
    start_new_thread(updateOne, (period, multiplier, currency, timeframe))

def pnl():
    while True:
        orderData = orderCheck()
        pnlUpdate(orderData)
        time.sleep(1)

def bot(period=period.get(), multiplier=multiplier.get(), currency=currency, timeframe=timeframe):
    data = run_superTrend(int(period), int(multiplier), currency, timeframe)
    dataWrite(data)
    timesc = int(timeframe[:-1]) * 60
    countdown(timesc, label12, timetext)
    time.sleep(1)
    while True:
        data = run_superTrend(int(period), int(multiplier), currency, timeframe)
        dataUpdate(data)
        timesc = int(timeframe[:-1])*60
        countdown(timesc, label12, timetext)
        time.sleep(1)

def mainThread(period=period.get(), multiplier=multiplier.get(), currency=currency, timeframe=timeframe):
    start_new_thread(bot, (period, multiplier, currency, timeframe))
    start_new_thread(pnl, ())

button = TkinterCustomButton(master=frame,
                             text="Run Bot",
                             width=150,
                             height=30,
                             corner_radius=75,
                             fg_color=entryBackground,
                             hover_color=hoverColor,
                             hover=True,
                             text_color=blackColor,
                             command=lambda: mainThread(period.get(), multiplier.get(), currency, timeframe))
button.place(relx=0.44, rely=0.25)

root.resizable(False, False)
root.mainloop()




