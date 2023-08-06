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


def test_order_item_list_create_shipment():
	"""
	Tests the OrderItemList_CreateShipment API Call
	"""

	helper.provision_store('OrderItemList_CreateShipment.xml')

	order_item_list_create_shipment_test_create_shipment()
	order_item_list_create_shipment_test_add_items_from_orderitem_instance()


def order_item_list_create_shipment_test_create_shipment():
	order = helper.get_order(678570)

	assert isinstance(order, merchantapi.model.Order)

	request = merchantapi.request.OrderItemListCreateShipment(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	for item in order.get_items():
		request.add_line_id(item.get_line_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListCreateShipment)

	assert isinstance(response.get_order_shipment(), merchantapi.model.OrderShipment)
	assert order.get_id() == response.get_order_shipment().get_order_id()
	assert response.get_order_shipment().get_id() > 0


def order_item_list_create_shipment_test_add_items_from_orderitem_instance():
	item1 = merchantapi.model.OrderItem({'line_id': 123})
	item2 = merchantapi.model.OrderItem({'line_id': 456})

	request = merchantapi.request.OrderItemListCreateShipment(helper.init_client())

	request.add_order_item(item1)\
		.add_order_item(item2)

	lines = request.get_line_ids()

	assert isinstance(lines, list)
	assert len(lines) == 2
	assert 123 in lines
	assert 456 in lines
