from django.http import HttpResponse
from django.http import JsonResponse

from .helpers.cryptocurrencies_helper import *

def index(request):
    return HttpResponse("Welcome the the currencies playground.")


'''
An endpoint for questions about cryptocurrencies

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
        considering the difference between the
        currency's value at the given date
        and the currency's value now.
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
        response = { "TO-DO" : "currency_date" }
    elif response_type == "currency_product":
        response = { "TO-DO" : "currency_product" }
    elif response_type == "currency_date_product":
        response = { "TO-DO" : "currency_date_product" }
    else:
        response = dict(msg="The only parameter required is currency. Ex(currency=BTC)")

    return JsonResponse(response)

