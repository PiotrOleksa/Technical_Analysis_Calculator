from ta.momentum import RSIIndicator
from ta.trend import MACD

import numpy as np
import pandas
from ta.volatility import BollingerBands


#---------------------Crypto class
class Crypto:
    def __init__(self, symbol):
        self.symbol = symbol
        self.technical_indicators = None
        self.prices = None


#--------------------- Buy and Sell Signals
def generate_buy_sell_signals(condition_buy, condition_sell, dataframe, strategy):
    last_signal = None
    indicators = []
    buy = []
    sell = []
    for i in range(0, len(dataframe)):
        if condition_buy(i, dataframe) and last_signal != 'Buy':
            last_signal = 'Buy'
            indicators.append(last_signal)
            buy.append(dataframe['Close'].iloc[i])
            sell.append(np.nan)
        elif condition_sell(i, dataframe)  and last_signal == 'Buy':
            last_signal = 'Sell'
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(dataframe['Close'].iloc[i])
        else:
            indicators.append(last_signal)
            buy.append(np.nan)
            sell.append(np.nan)

    dataframe[f'{strategy}_Last_Signal'] = np.array(last_signal)
    dataframe[f'{strategy}_Indicator'] = np.array(indicators)
    dataframe[f'{strategy}_Buy'] = np.array(buy)
    dataframe[f'{strategy}_Sell'] = np.array(sell)


#--------------------- Technical Indicators
def set_technical_indicators(config, crypto):
    crypto.technical_indicators = pandas.DataFrame()
    crypto.technical_indicators['Close'] = crypto.prices

    get_macd(config, crypto)
    get_rsi(config, crypto)
    get_bollinger_bands(config, crypto)


#--------------------- MACD
def get_macd(config, crypto):
    close_prices = crypto.prices
    dataframe = crypto.technical_indicators
    window_slow = 26
    signal = 9
    window_fast = 12
    macd = MACD(crypto.prices, window_slow, window_fast, signal)
    dataframe['MACD'] = macd.macd()
    dataframe['MACD_Histogram'] = macd.macd_diff()
    dataframe['MACD_Signal'] = macd.macd_signal()

    generate_buy_sell_signals(
        lambda x, dataframe: dataframe['MACD'].values[x] < dataframe['MACD_Signal'].iloc[x],
        lambda x, dataframe: dataframe['MACD'].values[x] > dataframe['MACD_Signal'].iloc[x],
        dataframe,
        'MACD')
    return dataframe


#--------------------- RSI
def get_rsi(config, crypto):
    close_prices = crypto.prices
    dataframe = crypto.technical_indicators
    rsi_time_period = 20

    rsi_indicator = RSIIndicator(close_prices, rsi_time_period)
    dataframe['RSI'] = rsi_indicator.rsi()

    low_rsi = 40
    high_rsi = 70

    generate_buy_sell_signals(
        lambda x, dataframe: dataframe['RSI'].values[x] < low_rsi,
        lambda x, dataframe: dataframe['RSI'].values[x] > high_rsi,
    dataframe, 'RSI')

    return dataframe


#--------------------- Bollinger Bands
def get_bollinger_bands(config, crypto):

    close_prices = crypto.prices
    dataframe = crypto.technical_indicators

    window = 20

    indicator_bb = BollingerBands(close=close_prices, window=window, window_dev=2)

    
    dataframe['Bollinger_Bands_Middle'] = indicator_bb.bollinger_mavg()
    dataframe['Bollinger_Bands_Upper'] = indicator_bb.bollinger_hband()
    dataframe['Bollinger_Bands_Lower'] = indicator_bb.bollinger_lband()


    generate_buy_sell_signals(
        lambda x, signal: signal['Close'].values[x] < signal['Bollinger_Bands_Lower'].values[x],
        lambda x, signal: signal['Close'].values[x] > signal['Bollinger_Bands_Upper'].values[x],
        dataframe, 'Bollinger_Bands')

    return dataframe
