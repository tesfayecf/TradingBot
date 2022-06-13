# tradingBot
Automated trading bot GUI in which custom strategies can be applied. Implemented in python using Binance API.

Graphic User Interface 

![image](https://user-images.githubusercontent.com/90719152/173408634-739e640a-070b-49fb-9fee-69903aba3d74.png)

Select the strategy parameters with the buttons above.

<img src="https://user-images.githubusercontent.com/90719152/173417459-3f66cab2-a867-4adc-b194-ca106583ef14.png" width="400px">

Press the "Run Bot" button to start the algorithm.

<img src="https://user-images.githubusercontent.com/90719152/173417809-0f30c579-c65a-48b0-9632-89bb9ea0e1e8.png" width="400px">

Live data will be displayed at the center of the window. 

<img src="https://user-images.githubusercontent.com/90719152/173418252-a6d69c83-da78-4a36-a790-4976dee021c7.png" width="400px">

If the plot button is pressed while the bot is active, a new window will appear with the live candlestick data displayed.

<img src="https://user-images.githubusercontent.com/90719152/173418439-47e870c5-299c-4af9-ad58-9aff9d61be28.png" width="400px">

Also, the update button resets the timer and the conditions are checked again.

<img src="https://user-images.githubusercontent.com/90719152/173419587-43fc7d3e-5a04-4d1f-8494-3c63c95d5d90.png" width="400px">

When a new order is triggered, the PNL of the position is displayed above the market data.

New strategies can be developed to be used with this interface. The main strategy is based on the supertrend indicator.

To build a new strategy create the following functions:
- get_(name): this function formats the data received from the API and calculates the necessary indicators the be checked.
- check_buy_sell_signals: check the necessary custom conditions that need to be fulfilled to trigger the algorithm.
- plot_(name): function to be invocked when the "plot" button is clicked. Set what and in which colors has to be plotted.
- run_(name): gathers and organizes all the functions above. It's called by the "Run Bot" button.

To create a new strategy import the new file and modify the function names into the App.py file.

To set up run:
```
pip install -r requirements
```

and change the config.py file parameters:
 ```
 BINANCE_API_KEY = ''
BINANCE_SECRET_KEY = ''
```

