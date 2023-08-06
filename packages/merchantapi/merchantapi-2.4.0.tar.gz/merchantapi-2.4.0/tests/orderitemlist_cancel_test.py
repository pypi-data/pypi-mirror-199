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


def test_order_item_list_cancel():
	"""
	Tests the OrderItemList_Cancel API Call
	"""

	helper.provision_store('OrderItemList_Cancel.xml')

	order_item_list_cancel_test_cancel()
	order_item_list_cancel_test_add_items_from_orderitem_instance()


def order_item_list_cancel_test_cancel():
	order = helper.get_order(678567)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 4

	request = merchantapi.request.OrderItemListCancel(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	request.set_reason('API Test')

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListCancel)

	order = helper.get_order(678567)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 4

	for item in order.get_items():
		assert isinstance(item, merchantapi.model.OrderItem)
		assert item.get_status() == merchantapi.model.OrderItem.ORDER_ITEM_STATUS_CANCELLED
		assert isinstance(item.get_options(), list)
		assert len(item.get_options()) == 1
		assert item.get_options()[0].get_attribute_code() == 'Cancellation Reason'
		assert item.get_options()[0].get_value() == 'API Test'


def order_item_list_cancel_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListCancel(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines
