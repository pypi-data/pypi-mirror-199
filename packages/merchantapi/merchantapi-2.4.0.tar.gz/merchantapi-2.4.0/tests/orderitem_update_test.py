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


def test_order_item_update():
	"""
	Tests the OrderItem_Update API Call
	"""

	helper.provision_store('OrderItem_Update.xml')

	order_item_update_test_update()
	order_item_update_test_update_with_existing_attribute()


def order_item_update_test_update():
	order = helper.get_order(678569)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 2

	item1 = order.get_items()[0]

	request = merchantapi.request.OrderItemUpdate(helper.init_client(), item1)

	assert request.get_line_id() == item1.get_line_id()

	request.set_order_id(order.get_id())\
		.set_line_id(item1.get_line_id())\
		.set_quantity(item1.get_quantity() + 1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemUpdate)


def order_item_update_test_update_with_existing_attribute():
	order = helper.get_order(678570)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item1 = order.get_items()[0]

	request = merchantapi.request.OrderItemUpdate(helper.init_client(), item1)

	assert request.get_line_id() == item1.get_line_id()
	assert isinstance(item1.get_options(), list)
	assert len(item1.get_options()) == 1
	assert isinstance(item1.get_options()[0], merchantapi.model.OrderItemOption)

	request.set_order_id(order.get_id())\
		.set_line_id(item1.get_line_id())\
		.set_quantity(item1.get_quantity() + 2)

	request.get_options()[0].set_value('BIN')\
		.set_price(29.99)\
		.set_weight(15.00)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemUpdate)

	order = helper.get_order(678570)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item = order.get_items()[0]

	assert isinstance(item, merchantapi.model.OrderItem)
	assert isinstance(item.get_options(), list)
	assert len(item.get_options()) == 1

	option = item.get_options()[0]

	assert isinstance(option, merchantapi.model.OrderItemOption)
	assert option.get_price() == 29.99
	assert option.get_weight() == 15.00
