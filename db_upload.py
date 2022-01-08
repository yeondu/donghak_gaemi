import os
import django
import csv
import sys

import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Donghakgaemi.settings")
django.setup()

from stock.models import *

CSV_PATH_PRODUCTS = 'stock/stock_price_API/yahoo_finance_API.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        date = pd.to_datetime(row[3])
        stockModel.objects.create(stock_name=row[1], stock_code=row[2], stock_category=date,
                                  stock_foundation_year=date, stock_listing_date=date)
        priceModel.objects.create(stock_id = row[0], date = date, open = row[4], high = row[5], low = row[6],
                                  close = row[7], adj_close = row[7], volume = row[8], stock_code = row[2])