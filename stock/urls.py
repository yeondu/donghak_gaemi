from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.home, name = 'list'),
    path('detail/<int:id>', views.detail_stock_news, name = 'detail'),
]