from pycoingecko import CoinGeckoAPI
import pandas as pd
pd.set_option('float_format', '{:.5f}'.format)



#---------------------------- API Call
cg = CoinGeckoAPI()


#---------------------------- Get Data
def crypto_data(crypto):
    list_crypto = cg.get_coins_list()
    df_crypto = pd.DataFrame(list_crypto)

    exec("%s = %d" % (crypto,2))
    lst_365 = cg.get_coin_market_chart_by_id(id=df_crypto['id'].loc[df_crypto['symbol'] == crypto].values[0], vs_currency='usd', days=365)
    prices = []
    time = []
    volume_to_marketcap = []
    for i in range(len(lst_365['prices'])):
        prices.append(lst_365['prices'][i][1])

    for i in range(len(lst_365['prices'])):
        time.append(int(lst_365['prices'][i][0]/1000))

    for i in range(len(lst_365['market_caps'])):
        volume_to_marketcap.append((lst_365['total_volumes'][i][1]+1)/(lst_365['market_caps'][i][1]+1))


    df = pd.DataFrame({'Date':time,
                       'Close': prices,
                       'V_to_M':volume_to_marketcap})
    df.index = pd.to_datetime(df['Date'], unit='s')
    vars()[crypto] = df.drop(columns=['Date'])
        
    return vars()[crypto]


    





