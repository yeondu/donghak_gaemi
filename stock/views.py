from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.views.generic import View
from time import mktime, strptime
from stock.models import stockModel, priceModel, predictModel, accuracyModel
from django.core.paginator import Paginator
# Create your views here.

# 종목 리스트
def home(request):
    MAX_LIST_CNT = 10 # 한 페이지에 보여주는 종목 수
    name = stockModel.objects.values('stock_name')
    r = []
    for n in name: # 주식 리스트 생성
        code = stockModel.objects.filter(stock_name=n['stock_name']).values('stock_code')[0]
        price_id = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('stock_id')[0] # 주가 아이디
        close = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('close')[0]
        before = priceModel.objects.filter(stock_code = code['stock_code']).order_by('-date').values('close')[1]
        fluc = (close['close'] - before['close'])/close['close']
        fluction = {'fluction':fluc}
        predict = predictModel.objects.filter(stock_id = price_id['stock_id']).values('result')[0]
        accuracy = accuracyModel.objects.filter(stock_code = code['stock_code']).order_by('-model_id').values('accuracy')[0]
        result = {**n, **code, **close, **predict, **accuracy, **price_id, **fluction}
        r.append(result)

    page = request.GET.get('page', 1)  # page 번호를 get 파라미터로 받고 없으면 기본값 1로 설정
    list = r
    paginator = Paginator(list, MAX_LIST_CNT)
    page_obj = paginator.get_page(page)
    context = {'page': page_obj}
    return render(request, 'stock/list.html', context)


# 종목 상세페이지(뉴스)
def detail_stock_news(request, id):
    price = priceModel.objects.get(stock_id = id)
    stock = price.stock_code
    #stock = stockModel.objects.filter(stock_code = price['stock_code_id']).values()
    return render(request, 'stock/detail.html', {'price':price, 'stock':stock})




