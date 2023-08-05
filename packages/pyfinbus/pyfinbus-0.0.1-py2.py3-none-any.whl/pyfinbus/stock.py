import datetime
import time
import pandas as pd

from pyfinbus.base import fetch_xueqiu
import pyfinbus.api_urls as api


def kline(symbol, start, end=None, period='day', rehab='before'):
    # parse date
    if end is None:
        end = int(time.time()) * 1000
    else:
        end_datatime = datetime.datetime.strptime(end, '%Y-%m-%d')
        end = int(time.mktime(end_datatime.timetuple())) * 1000

    start_datatime = datetime.datetime.strptime(start, '%Y-%m-%d')
    start = int(time.mktime(start_datatime.timetuple())) * 1000

    # concat url
    url = api.xueqiu_kline.format(symbol, start, end, period, rehab)

    # request
    json = fetch_xueqiu(url)

    return json


def valuation(symbol, type='ps'):
    # concat url
    url = api.xueqiu_valuation.format(symbol, type)

    # request
    json = fetch_xueqiu(url)
    return json
