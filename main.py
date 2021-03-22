from unittest import TestCase
from technical_indicators_calculator import set_technical_indicators, Crypto
from technical_indicators_chart_plotting import TechnicalIndicatorsChartPlotter
from crypto_data import crypto_data

print('Select a symbol of a cryptocurrency: ')
coin = input()
coin_1 = crypto_data(coin)

class TestTechnicalIndicator(TestCase):

    def test_tech_indicator():
        crypto = Crypto(f'{coin}')
        config = {}
        crypto.prices = coin_1['Close']
        set_technical_indicators(config, crypto)

        tacp = TechnicalIndicatorsChartPlotter()
        tacp.plot_macd(crypto)
        tacp.plot_rsi(crypto)
        tacp.plot_bollinger_bands(crypto)
        
TestTechnicalIndicator.test_tech_indicator()



