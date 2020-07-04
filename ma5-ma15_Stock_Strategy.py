import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import matplotlib.pyplot as plt
#print(plt.style.available)
plt.style.use('fivethirtyeight')

#Store the data into a dataframe
this_Stock = 'TSLA'
Stock = pd.read_csv('TSLA.csv')
#df = AAPL.set_index(pd.DatetimeIndex(Stock['Date'].values))
#Visualize the data
plt.figure(figsize=(14, 7))
plt.plot(Stock['Adj Close'], label=this_Stock)
plt.title(this_Stock +' Adj. Close Price History')
plt.xlabel('2019/07/03 -- 2020/07/01')
plt.ylabel('Adj. Close Price USD ($)')
plt.legend(loc='upper left')
#plt.show()

#Create the simple moving average with a 5 day window
SMA5 = pd.DataFrame()
print(Stock)
SMA5['Adj Close'] = Stock['Adj Close'].rolling(window=5).mean()

#Create a simple moving 20 day average
SMA15 = pd.DataFrame()
SMA15['Adj Close'] = Stock['Adj Close'].rolling(window=15).mean()

#Visualize the data
plt.figure(figsize=(14, 7))
plt.plot(Stock['Adj Close'], label=this_Stock)
plt.plot(SMA5['Adj Close'], label = 'SMA5')
plt.plot(SMA15['Adj Close'], label = 'SMA15')
plt.title('Apple Adj. Close Price History')
plt.xlabel('2019/07/03 -- 2020/07/01')
plt.ylabel('Adj. Close Price USD ($)')
plt.legend(loc='upper left')

#Create a new data frame to store all the data
data = pd.DataFrame()
data[this_Stock] = Stock['Adj Close']
data['SMA5'] = SMA5['Adj Close']
data['SMA15'] = SMA15['Adj Close']
print(len(data))

#Create a function to signal when to buy and sell the stock
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1
    for i in range(len(data)):
        if data['SMA5'][i] > data['SMA15'][i]:
            if flag != 1:
                sigPriceBuy.append(data[this_Stock][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA5'][i] < data['SMA15'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data[this_Stock][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)

#Store the buy and sell data into a variable
buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

#Visualize the data and the strategy to buy and sell the stock
plt.figure(figsize=(15, 7))
plt.plot(data[this_Stock], label=this_Stock, alpha=0.3)
plt.plot(data['SMA5'], label='SMA5', alpha=0.3)
plt.plot(data['SMA15'], Label='SMA15', alpha=0.3)
plt.scatter(data.index, data['Buy_Signal_Price'], label='Buy', marker = '^', color = 'green')
plt.scatter(data.index, data['Sell_Signal_Price'], label='Sell', marker='v', color='red')
plt.title(this_Stock +' Adj. Close Price History Buy & Sell Signals')
plt.xlabel('07/03/2019 - 0701/2020')
plt.ylabel('Adj. Close Price USD ($)')
plt.legend(loc='upper left')
plt.show()