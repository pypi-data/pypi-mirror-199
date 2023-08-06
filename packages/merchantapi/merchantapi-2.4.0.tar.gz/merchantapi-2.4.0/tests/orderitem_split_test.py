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


def test_order_item_split():
	"""
	Tests the OrderItem_Split API Call
	"""

	helper.provision_store('OrderItem_Split.xml')

	option_item_split_test_split()


def option_item_split_test_split():
	order = helper.get_order(895955)

	assert order is not None
	assert len(order.get_items()) == 1
	assert order.get_items()[0].get_quantity() == 4

	request = merchantapi.request.OrderItemSplit(helper.init_client())

	request.set_order_id(order.get_id())
	request.set_line_id(order.get_items()[0].get_line_id())
	request.set_quantity(2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemSplit)

	assert response.get_split_order_item() is not None
	assert response.get_split_order_item().get_original_order_item() is not None
	assert response.get_split_order_item().get_split_order_item() is not None
	assert response.get_split_order_item().get_original_order_item().get_quantity() == 2
	assert response.get_split_order_item().get_split_order_item().get_quantity() == 2
