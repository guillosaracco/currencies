import math
import time
import datetime
import requests


'''
Defines a helper class for the cryptocurrencies view
'''

class CryptocurrenciesHelper():

    SUPPORTED_CURRENCIES = ["BTC", "LTC", "ETH"]

    '''
    Determines what type of answer should be provided
    based on the parameters included in the request.

    Returns one of the following:
    currency
    currency_date
    currency_product
    currency_date_product
    params_not_provided
    '''
    @staticmethod
    def handle_request_params(params):
        if "currency" in params and "date" in params and "amz_product_id" in params:
            return "currency_date_product"
        elif "currency" in params and "date" in params:
            return "currency_date"
        elif "currency" in params and "amz_product_id" in params:
            return "currency_product"
        elif "currency" in params:
            return "currency"
        else:
            return "params_not_provided"


    '''
    Create response based on only having the currency
    parameter provided
    '''
    @staticmethod
    def response_for_currency(request):
        CH = CryptocurrenciesHelper

        (currency, msg) = CH.get_currency_from_request(request)

        if currency == None:
            return dict(msg=msg, response="error")

        (currency_value, msg) = CH.get_currency_value(currency)

        if currency_value == None:
            return dict(msg=msg, response="error")

        (product_price, amz_product_id, msg) = CH.get_amz_product_price()

        response = CH.build_response(currency, currency_value, product_price, amz_product_id)

        return response


    '''
    Create response based on only having the currency
    and date parameters provided
    '''
    @staticmethod
    def response_for_currency_date(request):
        CH = CryptocurrenciesHelper

        (currency, msg) = CH.get_currency_from_request(request)

        if currency == None:
            return dict(msg=msg, response="error")

        (timestamp, msg) = CH.get_date_timestamp_from_request(request)

        if timestamp == None:
            return dict(msg=msg, response="error")

        (currency_value, msg) = CH.get_currency_value(currency)

        if currency_value == None:
            return dict(msg=msg, response="error")

        (product_price, amz_product_id, msg) = CH.get_amz_product_price()

        response = CH.build_response(currency, currency_value, product_price, amz_product_id, timestamp)

        return response


    '''
    Create response based on only having the currency
    and amz_product_id parameters provided
    '''
    @staticmethod
    def response_for_currency_product(request):
        CH = CryptocurrenciesHelper

        (currency, msg) = CH.get_currency_from_request(request)

        if currency == None:
            return dict(msg=msg, response="error")

        (currency_value, msg) = CH.get_currency_value(currency)

        if currency_value == None:
            return dict(msg=msg, response="error")

        (product_price, amz_product_id, msg) = CH.get_amz_product_price(request.get("amz_product_id"))

        if product_price == None:
            return dict(msg=msg, response="error")

        response = CH.build_response(currency, currency_value, product_price, amz_product_id)

        return response


    '''
    Create response based on having the currency, date
    and amz_product_id parameters provided
    '''
    @staticmethod
    def response_for_currency_date_product(request):
        CH = CryptocurrenciesHelper

        (currency, msg) = CH.get_currency_from_request(request)

        if currency == None:
            return dict(msg=msg, response="error")

        (timestamp, msg) = CH.get_date_timestamp_from_request(request)

        if timestamp == None:
            return dict(msg=msg, response="error")

        (currency_value, msg) = CH.get_currency_value(currency)

        if currency_value == None:
            return dict(msg=msg, response="error")

        (product_price, amz_product_id, msg) = CH.get_amz_product_price(request.get("amz_product_id"))

        response = CH.build_response(currency, currency_value, product_price, amz_product_id, timestamp)

        return response


    '''
    Gets the currency value from the params dict
    Returns the name of the currency if it is one
    of the SUPPORTED_CURRENCIES.
    Otherwise, it returns None.
    '''
    @staticmethod
    def get_currency_from_request(request):
        CH = CryptocurrenciesHelper

        currency = request.get("currency")

        if currency in CH.SUPPORTED_CURRENCIES:
            return (currency, "")
        else:
            return (None, "This endpoint only supports the following cryptocurrencies: %s" % CH.SUPPORTED_CURRENCIES)


    '''
    Gets the date value from the params dict
    and converts it to epoch timestamp.

    Expects date format to be YYYY-MM-dd
    
    If timestamp is in the future, returns None.
    Else, returns timestamp

    If date cannot be converted to epoch,
    returns None.
    '''
    @staticmethod
    def get_date_timestamp_from_request(request):
        date_string = request.get("date")
        try:
            timestamp = time.mktime(datetime.datetime.strptime(date_string, "%Y-%m-%d").timetuple())
        except Exception:
            return (None, "Please input a date with format YYYY-MM-dd")
        else:
            if timestamp > time.mktime(datetime.datetime.now().timetuple()):
                return (None, "Date cannot be in the future.")
            else:
                return (timestamp, "")


    @staticmethod
    def build_response(currency, currency_value, product_price, amz_product_id, timestamp=None):
        CH = CryptocurrenciesHelper

        (units, change, msg) = CH.compare_currency_value_and_product_price(currency, currency_value, product_price, timestamp)

        response = dict(
                response="ok",
                data=dict(
                        amz_product_id=amz_product_id,
                        product_url="https://www.amazon.com/gp/product/" + amz_product_id,
                        units=units,
                        change=change,
                        msg=msg,
                    )
            )

        return response


    '''
    Given a currency_value and product_price, compares both values
    to determine:
    - how many units of the product can be bought.

    returns (units, change, msg)

    units: the number of units that can be bought with the currency_value.
    change: the spare change.
    msg:
        if currency_value >= product_price
            You can buy 248 units of the product with 1 BTC.
        else
            You need at least 3 LTC to buy 1 unit of the product.

    '''
    def compare_currency_value_and_product_price(currency, currency_value, product_price, timestamp=None):
        units = currency_value / product_price
        timestamp_now = time.mktime(datetime.datetime.now().timetuple())

        msg = ""

        if currency_value >= product_price:
            units_int = int(units)
            change = currency_value - (units_int * product_price)
            change = float("{0:.2f}".format(change))

            if timestamp != None:
                date_value = datetime.date.fromtimestamp(timestamp)
                msg = "You could have bought %s units of the product with 1 %s on %s." % (units_int, currency, date_value)
            else:
                msg = "You can buy %s units of the product with 1 %s." % (units_int, currency)

            return (units_int, change, msg)
        else:
            currency_units_needed = float("{0:.10f}".format(1/units))
            units = float("{0:.2f}".format(units))

            if timestamp != None:
                date_value = datetime.date.fromtimestamp(timestamp)
                msg = "You would have needed %s %s to buy one unit of the product on %s." % (currency_units_needed, currency, date_value)
            else:
                msg = "You need %s %s to buy one unit of the product." % (currency_units_needed, currency)
            return (units, 0, msg)


    '''
    Given a cryptocurrency, returns the current USD value.
    Ex: BTC -> 7533.53
    '''
    @staticmethod
    def get_currency_value(currency, timestamp=None):
        CH = CryptocurrenciesHelper

        if currency not in CH.SUPPORTED_CURRENCIES:
            return (None, "This endpoint only supports the following cryptocurrencies: %s" % CH.SUPPORTED_CURRENCIES)

        value = None
        if timestamp is not None:
            try:
                r = requests.get('https://min-api.cryptocompare.com/data/pricehistorical?fsym=%s&tsyms=USD&ts=%s' % (currency, timestamp))
                value = r.json().get(currency).get("USD")
            except Exception:
                return (None, "There was an error getting the currency value.")
        else:
            try:
                r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=USD' % currency)
                value = r.json().get("USD")
            except Exception:
                return (None, "There was an error getting the currency value.")


        return (value, "")


    '''
    Gets the price of an amazon product.

    If amz_product_id is provided,
    it will return the price for that product.

    If no product information is provided,
    it will return a random amz_product_id and its price.

    If amz_product_id is invalid, it returns an error message.
    '''
    @staticmethod
    def get_amz_product_price(amz_product_id=None):
        if amz_product_id is not None:
            return (29.99, amz_product_id, "")
        else:
            return (349.99, "ASD9UFJ90", "")