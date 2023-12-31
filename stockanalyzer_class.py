# -*- coding: utf-8 -*-
"""StockAnalyzer Class.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QA1RtFZncfPaDWEaLZb0IPB8ekoHMEBa
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from IPython.display import display
# %matplotlib inline


#The below functions is created to format the headings of each output section
def print_bold_heading(heading):
    print("\033[7;59m" + heading + "\033[0m")


#The class stockanalyzer is defined below

class stockanalyzer:
#The following __init__ functions declares the input and other objects used in the function
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None


#The following variables are declared to take input from the user when the class is being used
        start_date = ""
        end_date = ""
        ticker = ""


#This function downlaod the data from the yahoo finance library from specified start and end date
    def download_data(self):
        self.data = yf.download(self.ticker, self.start_date, self.end_date)


#This function takes a window size of 60 days to calculate the SMA, and gives the table of SMA of the last 20 days of the end_date specified
#The window size is decided by researching the best and most used window size used for SMA
    def get_sma(self, column, window_size):
        return self.data[column].rolling(window = window_size).mean()


#This function takes a span of 60 days to calculate the EMA, and gives the table of EMA of the last 20 days of the end_date specified.
#The span is decided by researching the best and most used span used for EMA
    def get_ema(self, column, span):
        return self.data[column].ewm(span = span, adjust = False).mean()


#This functions calculates the RSI of the stock price with a window size of 14
#It calculates the average gain and loss of index price
    def get_rsi(self, column, window = 14):
        price_diff = self.data[column].diff(1)
        gain = price_diff.where(price_diff > 0, 0)
        loss = -price_diff.where(price_diff < 0, 0)

        avg_gain = gain.rolling(window = window, min_periods = 1).mean()
        avg_loss = loss.rolling(window = window, min_periods = 1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def get_macd(self, column, short_window = 12, long_window = 26, signal_window = 9):
        short_ema = self.data[column].ewm(span = short_window, adjust = False).mean()
        long_ema = self.data[column].ewm(span = long_window, adjust = False).mean()

        macd_line = short_ema - long_ema
        signal_line = macd_line.ewm(span = signal_window, adjust = False).mean()
        histogram = macd_line - signal_line

        macd_data = pd.DataFrame({'MACD': macd_line, 'Signal': signal_line, 'Histogram': histogram})

        return macd_data

    def get_bollinger_bands(self, column, window = 20, k = 2):
        middle_band = self.data[column].rolling(window = window).mean()
        std_dev = self.data[column].rolling(window = window).std()

        upper_band = middle_band + k * std_dev
        lower_band = middle_band - k * std_dev

        bollinger_bands = pd.DataFrame({'MiddleBand': middle_band, 'UpperBand': upper_band, 'LowerBand': lower_band})

        return bollinger_bands

#This functions calculates the SMA relative to the closing stock price with a window size of 60 days
    def sma_price_plot(self, window_size = 60):

        print_bold_heading(" Simple Moving Averages (SMA) ")

        sma = self.get_sma('Close', window_size)

        plt.figure(figsize = (16, 8))
        sns.set(style = 'darkgrid')

        plt.plot(self.data.index, self.data['Close'], label = 'Price', linewidth = 2)
        plt.plot(self.data.index, sma, label = f'{window_size}-days SMA', linewidth = 2)

        plt.title(f'{self.ticker} Stock Price with {window_size}-days SMA', fontsize = 16)
        plt.xlabel('Date', fontsize = 12)
        plt.ylabel('Price in $', fontsize = 12)
        plt.legend(loc = 'best', fontsize = 12)

        sma_table = pd.DataFrame({'Date': self.data.index, 'SMA': sma}).tail(20)
        display(sma_table)

        plt.show()

        print("Simple Moving Averages (SMAs) are technical indicators used in trading to find momentum and trends. They are average of closing prices over a period, with short-term trends for short term and long-term trends for longer term. it is an uptrend when a stock price is above its SMA, and vice versa.")

        print("\n-----------------------------------------------------------------------------------------------------------\n")


#This functions calculates the EMA relative to the closing stock price with a span of 60 days
    def ema_price_plot(self, span = 60):

        print_bold_heading(" Exponential Moving Averages (EMA) ")

        ema = self.get_ema('Close', span)

        plt.figure(figsize = (16, 8))
        sns.set(style = 'darkgrid')

        plt.plot(self.data.index, self.data['Close'], label = 'Price', linewidth = 2)
        plt.plot(self.data.index, ema, label = f'{span}-days EMA', linewidth = 2)

        plt.title(f'{self.ticker} Stock Price with {span}-days EMA', fontsize = 16)
        plt.xlabel('Date', fontsize = 12)
        plt.ylabel('Price in $', fontsize = 12)
        plt.legend(loc = 'best', fontsize = 12)

        ema_table = pd.DataFrame({'Date': self.data.index, 'EMA': ema}).tail(20)
        display(ema_table)

        plt.show()

        print("Exponential Moving Averages (EMA) helps smooth out price data, which helps to identify trends and potential entry and exit points. EMA puts more weightage on recent prices, to make it an even better responsive indicator than SMA. Stronger trends are indicated by higher EMAs, while lower EMAs suggest downtrends. Crossovers of varied EMAs with different periods, signals a potential change in trends.")

        print("\n-----------------------------------------------------------------------------------------------------------\n")

#This functions calculates and plots the RSI relative to the closing stock price with a window of 14 days
    def rsi_price_plot(self, window = 14):

        print_bold_heading(" Relative Strength Index (RSI) ")

        rsi = self.get_rsi('Close', window)

        plt.figure(figsize = (15, 9))
        sns.set(style = 'darkgrid')

        plt.plot(self.data.index, self.data['Close'], label = 'Price', linewidth = 2)
        plt.plot(self.data.index, rsi, label = 'RSI', linestyle = '--', color = 'orange', linewidth = 2)

        plt.title(f'{self.ticker} Stock Price with {window}-days RSI', fontsize = 16)
        plt.xlabel('Date', fontsize = 12)
        plt.ylabel('Price in $', fontsize = 12)
        plt.legend(loc = 'best', fontsize = 12)

        rsi_table = pd.DataFrame({'Date': self.data.index, 'RSI': rsi}).tail(20)
        display(rsi_table)

        plt.show()

        print("The Relative Strength Index (RSI) measures the momentum of price changes. It oscillates between 0 and 100. When levels are above 70 it indicates overbought conditions i.e. potential sell signals, with levels below 30 indicating oversold conditions i.e. potential buy signals. it is also used to identify divergences. RSI is just one of the tools would be advised not to be used on its own when making investment decisions.")

        print("\n-----------------------------------------------------------------------------------------------------------\n")


#This functions calculates the MACD which is the difference between short and long-term EMAs
    def macd_price_plot(self, short_window = 12, long_window = 26, signal_window = 9):

        print_bold_heading(" Moving Average Convergence Divergence (MACD) ")

        macd_data = self.get_macd('Close', short_window, long_window, signal_window)

        plt.figure(figsize = (15, 9))
        sns.set(style = 'darkgrid')

        plt.plot(self.data.index, self.data['Close'], label = 'Price', linewidth = 2)
        plt.plot(macd_data.index, macd_data['MACD'], label = 'MACD Line', linestyle = '--', color = 'orange', linewidth = 2)
        plt.plot(macd_data.index, macd_data['Signal'], label = 'Signal Line', linestyle = '--', color = 'blue', linewidth = 2)
        plt.bar(macd_data.index, macd_data['Histogram'], label = 'Histogram', color = 'gray', alpha = 0.3)

        plt.title(f'{self.ticker} Stock Price with MACD', fontsize = 16)
        plt.xlabel('Date', fontsize = 12)
        plt.ylabel('Price in $', fontsize = 12)
        plt.legend(loc = 'best', fontsize = 12)

        macd_table = macd_data.tail(20)
        display(macd_table)

        plt.show()

        print("The Moving Average Convergence Divergence indicator is used to identify trends and could be used as potential buy/sell signals. It is found by calculating the difference between two moving averages, which shows momentum of the stock & direction of the trend. MACD, divergences, crossovers, and histogram analysis is used to make a decisions. A crossover below zero is considered bearish, while above zero is bullish. Additionally, a MACD line turning up from below zero indicates a potential buy sign")

        print("\n-----------------------------------------------------------------------------------------------------------\n")



#This functions plots the bollinger bands with a window size of 20 days and k of 2

    def bollinger_bands_price_plot(self, window = 20, k = 2):

        print_bold_heading(" Bollinger Bands ")

        bollinger_bands_data = self.get_bollinger_bands('Close', window, k)

        plt.figure(figsize = (15, 9))
        sns.set(style = 'darkgrid')

        plt.plot(self.data.index, self.data['Close'], label = 'Price', linewidth = 2)
        plt.plot(bollinger_bands_data.index, bollinger_bands_data['MiddleBand'], label = 'Middle Band', linestyle = '--', color = 'orange', linewidth = 2)
        plt.plot(bollinger_bands_data.index, bollinger_bands_data['UpperBand'], label ='Upper Band', linestyle = '--', color = 'blue', linewidth = 2)
        plt.plot(bollinger_bands_data.index, bollinger_bands_data['LowerBand'], label = 'Lower Band', linestyle = '--', color = 'blue', linewidth = 2)

        plt.fill_between(bollinger_bands_data.index, bollinger_bands_data['UpperBand'], bollinger_bands_data['LowerBand'], color = 'gray', alpha = 0.2, label = 'Bollinger Bands')

        plt.title(f'{self.ticker} Stock Price with Bollinger Bands', fontsize = 16)
        plt.xlabel('Date', fontsize = 12)
        plt.ylabel('Price in $', fontsize = 12)
        plt.legend(loc = 'best', fontsize = 12)

        bollinger_bands_table = bollinger_bands_data.tail(20)
        display(bollinger_bands_table)

        plt.show()

        print("Bollinger Bands is the area bound around the stock price line, to help indicate volatility & reversal of price reversals. The middle line is a moving average, while the upper and lower lines are single standard deviation away from price line. When prices touch the upper band, it suggests the stock may be overbought, and vice versa for the lower band.")

        print("\n-----------------------------------------------------------------------------------------------------------\n")

# Example usage:
start_date = '2020-01-01'
end_date = '2022-12-31'
ticker = 'MSFT'

stockanalyzer = stockanalyzer(ticker, start_date, end_date)
stockanalyzer.download_data()
stockanalyzer.sma_price_plot()
stockanalyzer.ema_price_plot()
stockanalyzer.rsi_price_plot()
stockanalyzer.macd_price_plot()
stockanalyzer.bollinger_bands_price_plot()

