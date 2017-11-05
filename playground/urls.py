from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cryptocurrencies$', views.cryptocurrencies, name='cryptocurrencies'),
]