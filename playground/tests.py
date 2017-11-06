from django.test import TestCase
from .helpers.cryptocurrencies_helper import *

class CryptocurrenciesHelperMethodsTests(TestCase):

    # Tests for handle_request_params
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


    # tests for currency_from_request
    def test_get_currency_from_request_with_supported_currency(self):
        """
        If request includes a supported currency, return the currency
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS", "date" : "2015-08-12"}
        self.assertEqual(CryptocurrenciesHelper.get_currency_from_request(params), ("BTC", ""))

    def test_get_currency_from_request_with_unsupported_currency(self):
        """
        If request does NOT include a supported currency, return an error msg
        """
        params = {"currency" : "AAAAA", "amz_product_id" : "B01MQWUXZS", "date" : "2015-08-12"}
        msg = "This endpoint only supports the following cryptocurrencies: %s" % CryptocurrenciesHelper.SUPPORTED_CURRENCIES
        self.assertEqual(CryptocurrenciesHelper.get_currency_from_request(params), (None, msg))


    # tests for get_date_timestamp_from_request
    def test_get_date_timestamp_from_request_with_valid_date(self):
        """
        If request includes a valid date, return the timestamp
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS", "date" : "2015-08-12"}
        self.assertEqual(CryptocurrenciesHelper.get_date_timestamp_from_request(params), (1439337600.0, ""))

    def test_get_date_timestamp_from_request_with_invalid_date(self):
        """
        If request includes an invalid date, return an error msg
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS", "date" : "2015-089-12"}
        self.assertEqual(CryptocurrenciesHelper.get_date_timestamp_from_request(params), (None, "Please input a date with format YYYY-MM-dd"))

    def test_get_date_timestamp_from_request_with_future_date(self):
        """
        If request includes a future date, return an error msg
        """
        params = {"currency" : "BTC", "amz_product_id" : "B01MQWUXZS", "date" : "2118-09-12"}
        self.assertEqual(CryptocurrenciesHelper.get_date_timestamp_from_request(params), (None, "Date cannot be in the future."))


    # tests for compare_currency_value_and_product_price
    def test_compare_currency_value_and_smaller_product_price(self):
        """
        If currency_value >= product_price, return tuple with the
        following format:
        (units, change, "You can buy 450 units of the product with 1 BTC.")
        """

        expected_result = (62, 100.97, "You can buy 62 units of the product with 1 BTC.")
        actual_result = CryptocurrenciesHelper.compare_currency_value_and_product_price('BTC', 7540.35, 119.99)
        self.assertEqual(expected_result, actual_result)

    def test_compare_currency_value_and_greater_product_price(self):
        """
        If currency_value < product_price, return tuple with the
        following format:
        (units, change, "You need 3 LTC to buy one unit of the product.")
        """

        expected_result = (0.46, 0, "You need 2.1907978821 LTC to buy one unit of the product.")
        actual_result = CryptocurrenciesHelper.compare_currency_value_and_product_price('LTC', 54.77, 119.99)
        self.assertEqual(expected_result, actual_result)

    def test_compare_currency_value_and_smaller_product_price_on_date(self):
        """
        If currency_value >= product_price, return tuple with the
        following format:
        (units, change, "You can buy 450 units of the product with 1 BTC.")
        """

        expected_result = (62, 100.97, "You could have bought 62 units of the product with 1 BTC on 2012-08-29.")
        actual_result = CryptocurrenciesHelper.compare_currency_value_and_product_price('BTC', 7540.35, 119.99, 1346236702)
        self.assertEqual(expected_result, actual_result)

    def test_compare_currency_value_and_greater_product_price_on_date(self):
        """
        If currency_value < product_price, return tuple with the
        following format:
        (units, change, "You need 3 LTC to buy one unit of the product.")
        """

        expected_result = (0.46, 0, "You would have needed 2.1907978821 LTC to buy one unit of the product on 2012-08-29.")
        actual_result = CryptocurrenciesHelper.compare_currency_value_and_product_price('LTC', 54.77, 119.99, 1346236702)
        self.assertEqual(expected_result, actual_result)


    # tests for get_currency_value
    def test_get_currency_value_just_currency(self):
        """
        If a valid currency value is provided,
        it should return a float value
        """
        currency = "BTC"
        (value, msg) = CryptocurrenciesHelper.get_currency_value(currency)
        self.assertIsInstance(value, float)
        self.assertGreater(value, 0)
        self.assertEqual(msg, "")

    def test_get_currency_value_unsupported_currency(self):
        """
        If an invalid currency value is provided,
        it should return an error message
        """
        currency = "AA"
        message = "This endpoint only supports the following cryptocurrencies: %s" % CryptocurrenciesHelper.SUPPORTED_CURRENCIES
        (value, msg) = CryptocurrenciesHelper.get_currency_value(currency)
        self.assertEqual(value, None)
        self.assertEqual(msg, message)

    def test_get_currency_value_currency_and_timestamp(self):
        """
        If a valid currency value and timestamp is provided,
        it should return a float value
        """
        currency = "BTC"
        timestamp = 1446236702
        (value, msg) = CryptocurrenciesHelper.get_currency_value(currency, timestamp)
        self.assertIsInstance(value, float)
        self.assertGreater(value, 0)
        self.assertEqual(msg, "")

    def test_get_currency_value_with_timestamp_and_unsupported_currency(self):
        """
        If a timestamp and an invalid currency value are provided,
        it should return an error message
        """
        currency = "AA"
        timestamp = 1446236702
        message = "This endpoint only supports the following cryptocurrencies: %s" % CryptocurrenciesHelper.SUPPORTED_CURRENCIES
        (value, msg) = CryptocurrenciesHelper.get_currency_value(currency, timestamp)
        self.assertEqual(value, None)
        self.assertEqual(msg, message)

    def test_get_currency_value_with_future_timestamp(self):
        """
        If a timestamp and an invalid currency value are provided,
        it should return the latest (a valid) price.
        """
        currency = "BTC"
        timestamp = 4046236702
        message = "There was an error getting the currency value."
        (value, msg) = CryptocurrenciesHelper.get_currency_value(currency, timestamp)
        self.assertIsInstance(value, float)
        self.assertGreater(value, 0)
        self.assertEqual(msg, "")


