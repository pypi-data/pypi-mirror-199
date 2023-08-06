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


def test_order_item_list_create_return():
	"""
	Tests the OrderItemList_CreateReturn API Call
	"""

	helper.provision_store('OrderItemList_CreateReturn.xml')

	order_item_list_create_return_create_return()
	order_item_list_create_return_invalid_order()
	order_item_list_create_return_invalid_line_ids()


def order_item_list_create_return_create_return():
	order = helper.get_order(529555)

	assert order is not None

	request = merchantapi.request.OrderItemListCreateReturn(helper.init_client(), order)

	assert request.get_order_id() == order.get_id()

	for item in order.get_items():
		request.add_order_item(item)

	assert len(request.get_line_ids()) == len(order.get_items())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemListCreateReturn)

	assert isinstance(response.get_order_return(), merchantapi.model.OrderReturn)
	assert response.get_order_return().get_status() == merchantapi.model.OrderReturn.ORDER_RETURN_STATUS_ISSUED


def order_item_list_create_return_invalid_order():
	request = merchantapi.request.OrderItemListCreateReturn(helper.init_client())
	request.set_order_id(999999999)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderItemListCreateReturn)


def order_item_list_create_return_invalid_line_ids():
	request = merchantapi.request.OrderItemListCreateReturn(helper.init_client())
	request.set_order_id(529555)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderItemListCreateReturn)


def test_order_return_list_received():
	"""
	Tests the OrderReturnList_Received API Call
	"""

	helper.provision_store('OrderReturnList_Received.xml')

	order_return_list_received_test_received_return()


def order_return_list_received_test_received_return():
	order = helper.get_order(529556)

	assert order is not None

	create_request = merchantapi.request.OrderItemListCreateReturn(helper.init_client(), order)

	assert create_request.get_order_id() == order.get_id()

	for item in order.get_items():
		create_request.add_order_item(item)

	assert len(create_request.get_line_ids()) == len(order.get_items())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.OrderItemListCreateReturn)

	assert isinstance(create_response.get_order_return(), merchantapi.model.OrderReturn)
	assert create_response.get_order_return().get_status() == merchantapi.model.OrderReturn.ORDER_RETURN_STATUS_ISSUED

	request = merchantapi.request.OrderReturnListReceived(helper.init_client())

	for item in order.get_items():
		received_return = merchantapi.model.ReceivedReturn()
		received_return.set_return_id(create_response.get_order_return().get_id())
		received_return.set_adjust_inventory(1)

		request.add_received_return(received_return)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderReturnListReceived)

	check_order = helper.get_order(order.get_id())

	assert check_order is not None

	for item in check_order.get_items():
		assert item.get_status() ==  merchantapi.model.OrderReturn.ORDER_RETURN_STATUS_RECEIVED
