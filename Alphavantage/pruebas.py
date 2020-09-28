from alpha_vantage import ALPHA
import pandas as pd


apikey = '75IFXNX9X3L07ON1'

ticker = 'IBM'
alph_class = ALPHA(apikey)


temp = alph_class.get_intraday(ticker)
tenp2 = alph_class.get_company_overview(ticker)
temp3 = alph_class.get_company_income_statement(ticker)


def get_annual_reports(temp3):
    
    annual_reports = pd.DataFrame(temp3['annualReports'])
    quarterly_reports = pd.DataFrame(temp3['quarterlyReports'])
