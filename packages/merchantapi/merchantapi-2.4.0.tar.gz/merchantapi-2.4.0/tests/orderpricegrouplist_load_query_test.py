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


def test_order_price_group_list_load_query():
	"""
	Tests the OrderPriceGroupList_Load_Query API Call
	"""

	helper.provision_store('OrderPriceGroupList_Load_Query.xml')

	order_price_group_list_load_query_test_list_load()


def order_price_group_list_load_query_test_list_load():
	order = helper.get_order(3651498)

	assert order is not None

	request = merchantapi.request.OrderPriceGroupListLoadQuery(helper.init_client(), order)

	request.set_assigned(True)
	request.set_unassigned(False)

	assert order.get_id() == request.get_order_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderPriceGroupListLoadQuery)

	assert len(response.get_order_price_groups()) == 2
	for order_price_group in response.get_order_price_groups():
		assert isinstance(order_price_group, merchantapi.model.OrderPriceGroup)
		assert order_price_group.get_name() in ('OrderPriceGroupListLoadQuery_1', 'OrderPriceGroupListLoadQuery_2')
