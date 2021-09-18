from django import template
from stock.models import priceModel, stockModel, predictModel, accuracyModel

register = template.Library()


@register.filter(name = 'reportkey')
def reportkey(value):
    r = []
    for n in value:
        stock = stockModel.objects.filter(stock_name = n['stock_name']).values()[0]
        price = priceModel.objects.filter(stock_code = stock['stock_code']).values()[0]
        price_id = priceModel.objects.filter(stock_code = stock['stock_code']).values('stock_id')[0]
        code = stockModel.objects.filter(stock_name = n['stock_name']).values('stock_code')[0]
        close = priceModel.objects.filter(stock_code = stock['stock_code']).values('close')[0]
        predict = predictModel.objects.filter(stock_id = price['stock_id']).values('result')[0]
        accuracy = accuracyModel.objects.filter(stock_code = stock['stock_code']).values('accuracy')[0]
        result = {**n, **code, **close, **predict, **accuracy, **price_id}
        r.append(result)
    return r