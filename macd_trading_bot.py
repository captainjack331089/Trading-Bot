#Description: This program uses the Moving Average Convergence/Divergence(MACD) crossover to determin when to buy and sell stock.

import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import matplotlib.pyplot as plt
#print(plt.style.available)
plt.style.use('dark_background')

#Store the data into a dataframe
df = pd.read_csv('TSLA.csv')
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
#print(df)
#Visually show the stock price
plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label='Close')
plt.xticks(rotation=45)
plt.title('Close Price History')
plt.xlabel('Date')
plt.ylabel('Price USD ($)')

#print(plt.show())

#Calculate the MACD and signal line indicators
#Calculate the short tem exponential moving average (EMA)
shortEMA = df.Close.ewm(span=12, adjust=False).mean()
#Calculate the long term exponential moving average (EMA)
LongEMA = df.Close.ewm(span=26, adjust=False).mean()
#Calculate the MACD line
MACD = shortEMA - LongEMA
#Calculate the signal line
signal = MACD.ewm(span=9, adjust=False).mean()

#plot the chart
plt.figure(figsize=(12.2, 4.5))
plt.plot(df.index, MACD, label = 'APPLE MACD', color='red')
plt.plot(df.index, signal, label='Signal Line', color='blue')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
#print(plt.show())

#Create new columns for the data
df['MACD'] = MACD
df['Signal Line'] = signal


# Create a function to signal when to buy and sell an asset
def buy_sell(signal):
    Buy = []
    Sell = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return (Buy, Sell)

#Create a buy and sell column
aa = buy_sell(df)
df['Buy_Signal_Price'] = aa[0]
df['Sell_Signal_Price'] = aa[1]

#Visually show the stock buy and sell signals
plt.figure(figsize=(14, 6))
plt.scatter(df.index, df['Buy_Signal_Price'], color='green', label='Buy', marker='^', alpha = 1)
plt.scatter(df.index, df['Sell_Signal_Price'], color='red', label='Sell', marker='v', alpha = 1)
plt.plot(df['Close'], label='Close Price', alpha = 0.35)
plt.title('Close Price Buy & Sell Signals')
#plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.legend(loc = 'upper left')
plt.show()