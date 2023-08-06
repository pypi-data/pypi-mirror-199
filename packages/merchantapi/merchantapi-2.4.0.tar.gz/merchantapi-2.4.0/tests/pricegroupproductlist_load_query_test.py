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


def test_price_group_product_list_load_query():
	"""
	Tests the PriceGroupProductList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupProductList_Load_Query.xml')

	price_group_product_list_load_query_test_list_load()


def price_group_product_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupProductListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupProductListLoadQueryTest') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupProductListLoadQuery)

	assert isinstance(response.get_price_group_products(), list)
	assert len(response.get_price_group_products()) == 5

	for i, pgp in enumerate(response.get_price_group_products()):
		assert isinstance(pgp, merchantapi.model.PriceGroupProduct)
		assert pgp.get_code() == 'PriceGroupProductListLoadQueryTest_0%d' % int(i+1)
		assert pgp.get_name() == 'PriceGroupProductListLoadQueryTest_0%d' % int(i+1)
