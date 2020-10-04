from alpha_vantage import ALPHA
import pandas as pd


apikey = '75IFXNX9X3L07ON1'

ticker = 'AAPL'
alph_class = ALPHA(apikey)


# temp = alph_class.get_intraday(ticker)
# tenp2 = alph_class.get_company_overview(ticker)
# temp3 = alph_class.get_company_income_statement(ticker)
# url = alph_class.get_current_url()
# url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=AAPL&apikey=75IFXNX9X3L07ON1'
# import requests
# import json
# req = requests.read(url.read())
# tempo = json.load(url.read())
# req = requests.get(url).json()


temp = alph_class.get_ohlcv_adjusted(ticker,outputsize='full')
url = alph_class.get_current_url()


temp2 = pd.read_csv(url)