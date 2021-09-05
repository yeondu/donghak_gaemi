from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import stockModel, priceModel
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic import View
from time import mktime, strptime
from .models import stockModel, priceModel, predictModel, accuracyModel

# Create your views here.

# 종목 리스트
def home(request):
    stock = stockModel.objects.all()
    price = priceModel.objects.all()
    pr = predictModel.objects.all()
    acc = accuracyModel.objects.all()

    list = {'stock_name':stock.stock_name,
            'stock_code':stock.stock_code,
            'close':price.close,
            'predict':pr.result,
            'accuracy':acc.result
            }

    return render(request, 'stock/list.html', list)

# 종목 상세페이지(뉴스)
def detail_stock_news(request):
    return render(request, 'stock/detail.html')




