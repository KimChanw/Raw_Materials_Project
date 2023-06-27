from django.urls import path

from RawMaterialsDashBoard import views

urlpatterns = [
    path('', views.index, name='index')
]