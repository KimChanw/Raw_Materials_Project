from django.urls import path

from RawMaterialsDashBoard import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gold_silver_prices', views.gold_silver_prices, name='gold_silver_price')
]