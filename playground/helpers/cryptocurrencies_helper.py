'''
Defines a helper class for the cryptocurrencies view
'''

class CryptocurrenciesHelper():

    SUPPORTED_CURRENCIES = ["BTC", "LTC", "ETH"]

    '''
    Determines what type of answer should be provided
    based on the parameters included in the request.

    Types of answers:
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
    Create response based on only having the currency parameter provided
    '''
    @staticmethod
    def response_for_currency(request):
        CH = CryptocurrenciesHelper

        currency = CH.get_currency_from_request(request)

        if currency == None:
            return { "msg" : "This endpoint only supports the following cryptocurrencies: %s" % CH.SUPPORTED_CURRENCIES }

        currency_value = CH.get_currency_value(currency)
        product_price = CH.get_amz_product_price()

        response = CH.build_response(currency_value, product_price)

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
            return currency
        else:
            return None



    @staticmethod
    def build_response(currency_value, product_price):
        response = dict(
                response="ok",
                data=dict(
                        product_id="B01MQWUXZS",
                        product_url="https://www.amazon.com/gp/product/B01MQWUXZS",
                        units=450,
                        change=0.12,
                        msg="You could buy 248 Apple Earports with 1 BTC",
                    )
            )

        return response


    '''
    Given a cryptocurrency, returns the current USD value.
    Ex: BTC -> 7533
    '''
    @staticmethod
    def get_currency_value(currency):
        return 7533.53


    '''
    Gets the price of an amazon product.

    If amz_product_id is provided,
    it will return the price for that product.
    If no product information is provided,
    it will return the price of a random amazon product.
    '''
    @staticmethod
    def get_amz_product_price(product=None):
        return 29.99