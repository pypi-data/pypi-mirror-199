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


def test_price_group_excluded_category_list_load_query():
	"""
	Tests the PriceGroupExcludedCategoryList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupExcludedCategoryList_Load_Query.xml')

	price_group_excluded_category_list_load_query_test_list_load()


def price_group_excluded_category_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupExcludedCategoryListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedCategoryListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'PriceGroupExcludedCategoryListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryListLoadQuery)

	assert len(response.get_price_group_categories()) == 3
