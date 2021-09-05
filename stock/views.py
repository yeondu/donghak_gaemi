from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import stockModel, priceModel
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic import View
from time import mktime, strptime
from .models import stockModel, priceModel

# Create your views here.

# 종목 리스트
def home(request):
    all_list = priceModel.objects.all()
    return render(request, 'stock/list.html', {'list':all_list})

# 종목 상세페이지(뉴스)
def detail_stock_news(request):
    return render(request, 'stock/detail.html')




