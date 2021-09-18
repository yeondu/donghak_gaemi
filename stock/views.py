from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.views.generic import View
from time import mktime, strptime
from stock.models import stockModel, priceModel, predictModel, accuracyModel
import pandas as pd
# Create your views here.

# 종목 리스트

def home(request):
    name = stockModel.objects.values('stock_name')
    return render(request, 'stock/list.html', {'name':name})


# 종목 상세페이지(뉴스)
def detail_stock_news(request, id):
    price = priceModel.objects.get(stock_id = id)
    stock = price.stock_code
    #stock = stockModel.objects.filter(stock_code = price['stock_code_id']).values()
    return render(request, 'stock/detail.html', {'price':price, 'stock':stock})




