"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
import time
import random
from . import helper


def test_order_item_list_back_order():
	"""
	Tests the OrderItemList_BackOrder API Call
	"""

	helper.provision_store('OrderItemList_BackOrder.xml')

	order_item_list_back_order_test_backorder()
	order_item_list_back_order_test_add_items_from_orderitem_instance()


def order_item_list_back_order_test_backorder():
	order = helper.get_order(678566)

	assert isinstance(order, merchantapi.model.Order)

	isdate = int(time.time()) + int(random.random() + 1000)

	request = merchantapi.request.OrderItemListBackOrder(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	request.set_date_in_stock(isdate)

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	assert len(order.get_items()) == len(request.get_line_ids())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListBackOrder)

	checkorder = helper.get_order(678566)

	assert isinstance(checkorder, merchantapi.model.Order)
	assert checkorder.get_date_in_stock() == isdate

	for item in checkorder.get_items():
		assert item.get_status() == merchantapi.model.OrderItem.ORDER_ITEM_STATUS_BACKORDERED


def order_item_list_back_order_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListBackOrder(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines
