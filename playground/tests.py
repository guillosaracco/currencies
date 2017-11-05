from django.test import TestCase
from .helpers.cryptocurrencies_helper import *

class CryptocurrenciesHelperMethodsTests(TestCase):

    def test_handle_request_params_with_no_params(self):
        """
        If no params provided in request, should return params_not_provided.
        """
        params = {}
        self.assertEqual(CryptocurrenciesHelper.handle_request_params(params), 'params_not_provided')

    def test_handle_request_params_with_only_currency(self):
        """
        If request only includes currency provided, should return currency
        """
        params = {"currency" : "BTC"}
        self.assertEqual(CryptocurrenciesHelper.handle_request_params(params), 'currency')

    def test_handle_request_params_with_currency_and_date(self):
        """
        If request only includes currency and date, should return currency_date
        """
        params = {"currency" : "BTC", "date" : "2015-08-12"}
        self.assertEqual(CryptocurrenciesHelper.handle_request_params(params), 'currency_date')

    def test_handle_request_params_with_currency_and_product_id(self):
        """
        If request only includes currency and amz_product_id, should return currency_product
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS"}
        self.assertEqual(CryptocurrenciesHelper.handle_request_params(params), 'currency_product')

    def test_handle_request_params_with_currency_and_product_id_and_date(self):
        """
        If request includes currency, amz_product_id and date, should return currency_date_product
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS", "date" : "2015-08-12"}
        self.assertEqual(CryptocurrenciesHelper.handle_request_params(params), 'currency_date_product')


    def test_get_currency_from_request(self):
        """
        If request includes a supported currency, return the currency
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS", "date" : "2015-08-12"}
        self.assertEqual(CryptocurrenciesHelper.get_currency_from_request(params), 'BTC')

    def test_get_currency_from_request(self):
        """
        If request does NOT include a supported currency, return None
        """
        params = {"currency" : "AAAAA", "amz_product_id" : "B01MQWUXZS", "date" : "2015-08-12"}
        self.assertEqual(CryptocurrenciesHelper.get_currency_from_request(params), None)