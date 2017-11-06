<h1>Welcome to Currencies Playground</h1>

<p>You can find an endpoint for requests about cryptocurrencies <a href="{% url 'playground:cryptocurrencies' %}">RIGHT HERE</a></p>

<p>A request can have parameters such as:</p>
<ul>
  <li>currency=BTC</li>
  <li>date=YYYY-MM-DD</li>
  <li>amz_product_id=B01MQWUXZS</li>
</ul>

<p>The only parameter required is currency.</p>

<p>This endpoint will respond in the following different
ways based on the parameters provided.</p>

<p><b>currency</b> -> returns the number of units of a random product that can be bought from amazon considering the currency's actual value</p>

<p><b>currency + date</b> -> returns the number of units of a random product that can be bought from amazon considering the currency's value at the given date.</p>

<p>if amz_product_id is provided, the endpoint will return results with respect to that product.</p>
