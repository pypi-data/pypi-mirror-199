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


def test_price_group_excluded_product_list_load_query():
	"""
	Tests the PriceGroupExcludedProductList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupExcludedProductList_Load_Query.xml')

	price_group_excluded_product_list_load_query_test_list_load()


def price_group_excluded_product_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupExcludedProductListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedProductListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'PriceGroupExcludedProductListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedProductListLoadQuery)

	assert len(response.get_price_group_products()) == 3
