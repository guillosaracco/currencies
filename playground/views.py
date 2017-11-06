from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from .helpers.cryptocurrencies_helper import *

'''
Shows welcome page
'''
def index(request):
    return render(request, 'playground/index.html')


'''
An endpoint for requests about cryptocurrencies

A request can have parameters such as:
currency=BTC
date=YYYY-MM-DD
amz_product_id=B01MQWUXZS

The only parameter required is currency.

This endpoint will respond in the following different
ways based on the parameters provided.

currency
    -> returns the number of units of a random
        product that can be bought from amazon
        considering the currency's actual value
currency + date
    -> returns the number of units of a random
        product that can be bought from amazon
        considering the currency's value at
        the given date.
if amz_product_id is provided,
the endpoint will return results with respect
to that product.
'''
def cryptocurrencies(request):
    CH = CryptocurrenciesHelper

    response = {}
    params = request.GET

    response_type = CH.handle_request_params(params)

    if response_type == "currency":
        response = CH.response_for_currency(params)
    elif response_type == "currency_date":
        response = CH.response_for_currency_date(params)
    elif response_type == "currency_product":
        response = CH.response_for_currency_product(params)
    elif response_type == "currency_date_product":
        response = CH.response_for_currency_date_product(params)
    else:
        response = dict(msg="The only parameter required is currency. Ex(currency=BTC)")

    return JsonResponse(response)

