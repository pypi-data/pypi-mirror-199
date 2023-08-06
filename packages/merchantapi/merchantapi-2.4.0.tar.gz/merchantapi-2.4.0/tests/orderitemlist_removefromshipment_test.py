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


def test_order_item_list_remove_from_shipment():
	"""
	Tests the OrderItemList_RemoveFromShipment API Call
	"""

	helper.provision_store('OrderItemList_RemoveFromShipment.xml')

	order_item_list_remove_from_shipment_test_remove()


def order_item_list_remove_from_shipment_test_remove():
	order = helper.get_order(855855)

	assert order is not None
	assert len(order.get_items()) == 4

	shipments = helper.get_order_shipments(order.get_id())

	assert len(shipments) == 1

	request = merchantapi.request.OrderItemListRemoveFromShipment(helper.init_client(), order)

	request.add_order_item(order.get_items()[0])
	request.add_order_item(order.get_items()[1])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListRemoveFromShipment)

	check_order = helper.get_order(order.get_id())

	assert shipments[0].get_id() != check_order.get_items()[0].get_shipment_id()
	assert shipments[0].get_id() != check_order.get_items()[1].get_shipment_id()
