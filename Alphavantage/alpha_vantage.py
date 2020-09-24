import pandas as pd
import requests
import json


class ALPHA:

    def __init__(self, apikey):
        self.url_base = 'https://www.alphavantage.co/query?'
        self.apikey = apikey

    def retrieve_data_from_csv_to_pandas(self):
        retrieved_data = pd.read_csv(self.url)
        return retrieved_data

    def retrieve_json_to_dict(self):
        req = requests.get(self.url).content
        retrieved_data = json.loads(req)
        return retrieved_data

    def get_intraday(self, symbol, interval='5min',
                     adjusted='true', outputsize='compact', datatype='csv'):
        self.function = 'TIME_SERIES_INTRADAY'
        self.symbol = symbol
        self.interval = interval
        self.adjusted = adjusted
        self.outputsize = outputsize
        self.datatype = datatype

        self.url = self.url_base + 'function=' + self.function + '&' + 'symbol=' + self.symbol + '&' + 'interval=' + self.interval + '&' + \
            'apikey=' + self.apikey + '&' + 'adjusted=' + self.adjusted + '&' + \
            'outputsize=' + self.outputsize + '&' + 'datatype=' + self.datatype
        print(self.url)
        return self.retrieve_data_from_csv_to_pandas()

    def get_intraday_extended(self, symbol, interval='5min', slice='year1month1', adjusted='true'):
        self.function = 'TIME_SERIES_INTRADAY_EXTENDED'
        self.symbol = symbol
        self.interval = interval
        self.adjusted = adjusted
        self.slice = slice
        self.url = self.url_base + 'function=' + self.function + '&' + 'symbol=' + self.symbol + '&' + 'interval=' + self.interval + '&' + \
            'apikey=' + self.apikey + '&' + 'adjusted=' + self.adjusted + '&' + \
            'slice=' + self.slice
        self.retrieve_data_from_csv_to_pandas()

    def get_ohlcv(self, symbol, outputsize='compact', datatype='csv'):
        self.function = 'TIME_SERIES_DAILY'
        self.symbol = symbol
        self.outputsize = outputsize
        self.datatype = datatype
        self.url = self.url_base + 'function=' + self.function + '&' + 'symbol=' + self.symbol + '&' + 'outputsize=' + self.outputsize + '&' + \
            'apikey=' + self.apikey + '&' + 'datatype=' + self.datatype
        self.retrieve_data_from_csv_to_pandas()

    def get_ohlcv_adjusted(self, symbol, outputsize='compact', datatype='csv'):
        self.function = 'TIME_SERIES_DAILY'
        self.symbol = symbol
        self.outputsize = outputsize
        self.datatype = datatype
        self.url = self.url_base + 'function=' + self.function + '&' + 'symbol=' + self.symbol + '&' + 'outputsize=' + self.outputsize + '&' + \
            'apikey=' + self.apikey + '&' + 'datatype=' + self.datatype
        self.retrieve_data_from_csv_to_pandas()

    def get_company_overview(self, symbol):
        self.function = 'OVERVIEW'
        self.symbol = symbol

        self.url = self.url_base+'function=' + self.function + '&' + \
            'symbol=' + self.symbol + '&' + 'apikey=' + self.apikey
        return self.retrieve_json_to_dict()

    def get_company_income_statement(self, symbol):
        self.function = 'INCOME_STATEMENT'
        self.symbol = symbol

        self.url = self.url_base+'function=' + self.function + '&' + \
            'symbol=' + self.symbol + '&' + 'apikey=' + self.apikey
        return self.retrieve_json_to_dict()

    def get_company_balance_sheet(self, symbol):
        self.function = 'BALANCE_SHEET'
        self.symbol = symbol

        self.url = self.url_base+'function=' + self.function + '&' + \
            'symbol=' + self.symbol + '&' + 'apikey=' + self.apikey
        return self.retrieve_json_to_dict()

    def get_company_cash_flow(self, symbol):
        self.function = 'CASH_FLOW'
        self.symbol = symbol

        self.url = self.url_base+'function=' + self.function + '&' + \
            'symbol=' + self.symbol + '&' + 'apikey=' + self.apikey
        return self.retrieve_json_to_dict()
