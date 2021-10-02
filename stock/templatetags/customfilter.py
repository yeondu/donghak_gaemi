from django import template
from stock.models import priceModel, stockModel, predictModel, accuracyModel

register = template.Library()


@register.filter(name = 'reportkey')
def reportkey(value):
    r = []
    for n in value:
        stock = stockModel.objects.filter(stock_name = n['stock_name']).values()[0] # 해당 종목 정보
        price = priceModel.objects.filter(stock_code = stock['stock_code']).values()[0] # 해당 주가 정보
        price_id = priceModel.objects.filter(stock_code = stock['stock_code']).values('stock_id')[0] # 주가 아이디
        code = stockModel.objects.filter(stock_name = n['stock_name']).values('stock_code')[0]
        close = priceModel.objects.filter(stock_code = stock['stock_code']).order_by('-date').values('close')[0]
        before = priceModel.objects.filter(stock_code = stock['stock_code']).order_by('-date').values('close')[1]
        fluc = (close['close'] - before['close'])/close['close']
        fluction = {'fluction':fluc}
        predict = predictModel.objects.filter(stock_id = price['stock_id']).values('result')[0]
        accuracy = accuracyModel.objects.filter(stock_code = stock['stock_code']).values('accuracy')[0]
        result = {**n, **code, **close, **predict, **accuracy, **price_id, **fluction}
        r.append(result)
    return r