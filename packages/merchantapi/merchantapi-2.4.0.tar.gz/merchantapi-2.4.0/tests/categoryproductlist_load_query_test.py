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


def test_category_product_list_load_query():
	"""
	Tests the CategoryProductList_Load_Query API Call
	"""

	helper.provision_store('CategoryProductList_Load_Query.xml')

	category_product_list_load_query_test_list_load()


def category_product_list_load_query_test_list_load():
	request = merchantapi.request.CategoryProductListLoadQuery(helper.init_client())

	request.set_edit_category('CategoryProductListLoadQueryTest_Category') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryProductListLoadQuery)

	assert isinstance(response.get_category_products(), list)
	assert len(response.get_category_products()) == 3

	for i, cp in enumerate(response.get_category_products()):
		assert isinstance(cp, merchantapi.model.CategoryProduct)
		assert cp.get_code() == 'CategoryProductListLoadQueryTest_Product_%d' % int(i+1)
