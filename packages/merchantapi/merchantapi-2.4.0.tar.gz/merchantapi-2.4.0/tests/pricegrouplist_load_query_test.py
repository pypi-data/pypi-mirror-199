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


def test_price_group_list_load_query():
	"""
	Tests the PriceGroupList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupList_Load_Query.xml')

	price_group_list_load_query_test_list_load()


def price_group_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('name', 'PriceGroupListLoadQueryTest_%')) \
		.set_sort('id', merchantapi.request.PriceGroupListLoadQuery.SORT_ASCENDING)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupListLoadQuery)

	assert isinstance(response.get_price_groups(), list)
	assert len(response.get_price_groups()) == 14

	for i, pg in enumerate(response.get_price_groups()):
		assert isinstance(pg, merchantapi.model.PriceGroup)
		assert pg.get_name() == 'PriceGroupListLoadQueryTest_%d' % int(i+1)
