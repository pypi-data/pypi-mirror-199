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


def test_related_product_list_load_query():
	"""
	Tests the RelatedProductList_Load_Query API Call
	"""

	helper.provision_store('RelatedProductList_Load_Query.xml')

	related_product_list_load_query_test_list_load()


def related_product_list_load_query_test_list_load():
	product = helper.get_product('RelatedProductListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.RelatedProductListLoadQuery(helper.init_client(), product)

	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.RelatedProductListLoadQuery)

	assert len(response.get_related_products()) == 5

	for r in response.get_related_products():
		assert 'RelatedProductListLoadQueryTest_1' in r.get_code()
