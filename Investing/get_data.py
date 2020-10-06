# %%
# Libraries
# from urllib.request import Request, urlopen
# import urllib
from bs4 import BeautifulSoup as bs
from pandas.tseries.offsets import BDay
# from functools import partial
# import itertools
# import multiprocessing as mp
import requests
import datetime
import os
import investpy
import re
import pandas as pd
import numpy as np
import time
# import matplotlib.pyplot as plt
# from random import sample
# from tqdm import tqdm, tqdm_notebook
import random
# import math
# import xlsxwriter

# import sys
# import seaborn as sns

# %%
# Variables
nombres_indices = ["Euro Stoxx 50", "IBEX 35", "S&P 500", "DAX", "Bovespa", "Nikkei 225", "Reino Unido 100",
                   "Dow Jones Industrial Average", "IBEX Medium Cap", "IBEX Small Cap", "Hang Seng"]
tickers_indices = ["STOXX50E", "IBEX", "SPX", "GDAXI",
                   "BVSP", "N225", "invuk100", "DJI", "IBEXC", "IBEXS", "HSI"]
urls_indices = ["https://es.investing.com/indices/eu-stoxx50-components", "https://es.investing.com/indices/spain-35-components",
                "https://es.investing.com/indices/us-spx-500-components", "https://es.investing.com/indices/germany-30-components",
                "https://es.investing.com/indices/bovespa-components", "https://es.investing.com/indices/japan-ni225-components",
                "https://es.investing.com/indices/investing.com-uk-100-components", "https://es.investing.com/indices/us-30-components",
                "https://es.investing.com/indices/ibex-medium-cap-components", "https://es.investing.com/indices/ibex-small-cap-components",
                "https://es.investing.com/indices/hang-sen-40-components"]

tabla_indices = pd.DataFrame(
    list(zip(nombres_indices, tickers_indices, urls_indices)), columns=['nombres_indices', 'tickers_indices', 'urls_indices'])
tabla_indices
ventana = 30
# date_time_str = "01/01/2018"
# fecha_inicio = "01/01/1990"
# fecha_fin = "27/07/2020"
fecha_inicio = "01/01/2018"
fecha_fin = "31/12/2018"
ventana = 30
entrada = 0.15
salida = 0.85
percentil_dinamico = True
comision = 0.0008
comision_minima = 8
beneficio_objetivo_por_operacion = 100
stop_loss = 5
asignacion_maxima = 50000
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%d/%m/%Y')
fecha_fin = datetime.datetime.strptime(fecha_fin, '%d/%m/%Y')
Downloaded_files_path = r'C:\Users\arodr\Google Drive\Master_MIAX\hist_data\investing'
indice = tabla_indices.loc[1, 'urls_indices']
url = indice


def encontrar_fecha_anterior_inicio(fecha_inicio, ventana):
    """ Finds previous starting date

    args:
        fecha_inicio(dateTime): start date
        ventana(int):window size
        """
    fecha_anterior_inicio = fecha_inicio - BDay(ventana*2)
    return fecha_anterior_inicio


def composicion_indice(url):
    """ Returns a dataframe with the name of stocks and url for a given url index. 

    args:
        url(string): index investing.com url
        
    """
    html_requested_data = requests.get(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = bs(html_requested_data.content, 'html.parser')
# Write html to csv
# html = webpage.prettify("utf-8")
# with open("output1.html", "wb") as file:
#     file.write(html)

    data = []

    table = webpage.find("table", {'id': 'cr1'})
    rows = table.find_all('tr')
    for row in rows[1:len(rows)]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # Select column tables
        temp_data = [ele for ele in cols if ele]
        # Add link to the asset
        temp_link = row.find('a')['href']
        if('?cid=' in temp_link):
            p = re.compile('\?cid=\d*')
            c_id = p.findall(temp_link)
            link = temp_link.replace(c_id[0], '')
            temp_data.append('https://es.investing.com' +
                             link + '-historical-data'+c_id[0])
            print(f'https://es.investing.com{link}-historical-data{c_id[0]}')
        else:
            temp_data.append('https://es.investing.com' +
                             temp_link + '-historical-data')

        data.append(temp_data)
        # data.append([ele for ele in cols if ele],cols.find('a')['href'])

    header = rows[0].find_all('th')
    header_item = [ele.text.strip() for ele in header]
    header_items = header_item[1:(len(header_item)-1)]
    header_items.append('link')

    index_components = pd.DataFrame(data, columns=header_items)

    return index_components.loc[:, ['Nombre', 'link']]


def construimos_tabla_activos(item_link):
    time.sleep(random.randint(1, 2))
    html_requested_data = requests.get(
        item_link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = bs(html_requested_data.content, 'html.parser')

    temp_ticker = str(webpage.find_all(
        'h1', {'class': 'float_lang_base_1 relativeAttr'}))
    ticker = temp_ticker[temp_ticker.find("(")+1:temp_ticker.find(")")]
    stock_data = webpage.find('div', {'class': 'instrumentDataFlex'})
    currency = stock_data.find_all('span', {'class': 'bold'})[-1].text

    ISIN = stock_data.find_all(
        'span', {'class': 'elp'}, text=True)[2].text.replace(u'\xa0', u'')
    temp_market = stock_data.find_all('span', {'class': 'elp'})[1]
    temp_market = temp_market.find('a')['href']

    market = temp_market.replace('/markets/', '').replace(u'-', u' ')

    return([ticker, currency, ISIN, market])


def obtener_info_activos(indice):
    # Obtenemos los activos que componen cada índice.
    info_activos = composicion_indice(indice)
    info_activos["ticker"] = ""
    info_activos["currency"] = ""
    info_activos["ISIN"] = ""
    info_activos["market"] = ""
    # item_link = nombre_activos.iloc[1,1]
    # item = construimos_tabla_activos(item_link)

    info_activos[["ticker", "currency", "ISIN", "market"]] = info_activos.apply(
        lambda x: construimos_tabla_activos(x['link']), axis=1, result_type='expand')
    return info_activos


def descargar_cotizaciones_diarias_investing(url_activo, fecha_inicio, fecha_fin):
    # url_activo = url_activo['link']
    # Es el endpoint con la información a la que atacar (PHPSESSID y StickySession)
    uri = "https://es.investing.com/instruments/HistoricalDataAjax"
    data = []
    headers = {
        'Origin': "https://es.investing.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "text/plain, */*;",
        'Referer': url_activo,
        'X-Requested-With': "XMLHttpRequest"
    }
    # Obtenemos las coockies
    try:
        r = requests.get(url_activo, headers={'User-Agent': 'Mozilla/5.0'})
        PHPSESSID = r.cookies.get_dict()['PHPSESSID']
        StickySession = r.cookies.get_dict()['StickySession']

        html_requested_data = requests.get(
            url_activo, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = bs(html_requested_data.content, 'html.parser')

        wepage_str = webpage.prettify()
        posicion = wepage_str.find('smlId')
        smlId = re.findall('[0-9]+', wepage_str[posicion:(posicion+18)])[0]
        pairId = re.findall('[0-9]+', wepage_str[posicion-28:(posicion-1)])[0]

        payload = "curr_id="+pairId+"&smlID="+smlId+"&st_date=" + \
            fecha_inicio.strftime('%d') + '%2F'+fecha_inicio.strftime('%m') + \
            "%2F"+fecha_inicio.strftime('%Y')+"&end_date=" + \
            fecha_fin.strftime('%d')+"%2F"+fecha_fin.strftime('%m')+"%2F" + \
            fecha_fin.strftime('%Y') + \
            "&interval_sec=Daily&action=historical_data"
        response = requests.post(uri, data=payload, headers=headers)

        # SCRAPPING TABLE

        data_requested = bs(response.content, 'html.parser')
        table = data_requested.find("table", {'id': 'curr_table'})
        rows = table.find_all('tr')
        for row in rows[1:len(rows)]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            temp_data = [ele for ele in cols if ele]

            data.append(temp_data)

            temp = rows[0].find_all('th')
            temp = [ele.text.strip() for ele in temp]
            temp = temp[0:(len(temp))]
            cotizaciones = pd.DataFrame(data, columns=temp)

        cotizaciones = cotizaciones.iloc[:, :-1]

        # ERROR HANDLING
    except Exception:
        print("could not scrap data for url " + url_activo)
        emptylist = []
        cotizaciones = pd.DataFrame(emptylist)
        pass
    return cotizaciones


def get_cookie_value(r):
    return {'B': r.cookies['B']}


def descargar_cotizaciones_diarias_investing_api(info_activos, fecha_inicio, fecha_fin):

    data = investpy.get_stock_historical_data(
        'ACS', 'spain', '01/01/2019', '31/12/2019')

    data = investpy.get_stock_historical_data(
        stock=info_activos['ticker'], country=info_activos['market'], from_date=fecha_inicio.strftime('%d/%m/%Y'), to_date=fecha_fin.strftime('%d/%m/%Y'), order='descending')
    data['Fecha'] = data.index
    cols = ['Fecha', 'Close', 'Open', 'High', 'Low', 'Volume']
    data = data[cols]
    data.reset_index(drop=True, inplace=True)
    data.columns = ['Fecha', 'Último', 'Apertura', 'Máximo', 'Mínimo', 'Vol.']
    return data
