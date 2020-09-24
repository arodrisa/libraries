from alpha_vantage import ALPHA
import sys
print(sys.path)


apikey = '75IFXNX9X3L07ON1'

ticker = 'AAPL'
alph_class = ALPHA(apikey)


temp = alph_class.get_intraday(ticker)
tenp2 = alph_class.get_company_overview(ticker)