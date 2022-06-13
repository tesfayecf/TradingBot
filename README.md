# tradingBot
Automated trading bot GUI in which custom strategies can be applied. Implemented in python using Binance API.

Graphic User Interface 

![image](https://user-images.githubusercontent.com/90719152/173408634-739e640a-070b-49fb-9fee-69903aba3d74.png)

Select the strategy parameters with the buttons above.

Press the "Run Bot" button to strat the algorithm.

Live data will be displayed at the center of the window. 

If the plot button is pressed while the bot is active, a new window will appear with the live candlestick data displayed.

Also, the update button resets the timer and the conditions are checked again.

New strategies can be developed to be used with this interface. 

The main strategy is based on the supertrend indicator.

To build a new strategy create the following functions:
- get_(name): this function formats the data recievied from the api and calculets the necessary indicators the be checked.
- check_buy_sell_signals: check the necessary custom conditions that need to be fullfilled to trigger the algorithm.
- plot_(name): function to be called when the "plot" button is pressed. Set what has to be plotted and in which colors.
- run_(name): gathers and organizes all the functions above is is called by the "Run Bot" button.

To create a new strategy import the new file and change change the function names in the App.py file.

To set up run:
```
pip install -r requirements
```

and change the config.py file:
 ```
 BINANCE_API_KEY = ''
BINANCE_SECRET_KEY = ''
```

