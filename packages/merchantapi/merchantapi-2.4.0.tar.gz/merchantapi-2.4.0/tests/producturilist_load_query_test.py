"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
from . import helper


def test_product_uri_list_load_query():
	"""
	Tests the ProductURIList_Load_Query API Call
	"""

	helper.provision_store('ProductURIList_Load_Query.xml')

	product_uri_list_load_query_test_list_load()


def product_uri_list_load_query_test_list_load():
	product = helper.get_product('ProductURIListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.ProductURIListLoadQuery(helper.init_client(), product)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIListLoadQuery)

	assert len(response.get_uris()) > 1

	for uri in response.get_uris():
		assert uri.get_product_id() == product.get_id()
		if not uri.get_canonical():
			assert 'ProductURIListLoadQueryTest' in uri.get_uri()
