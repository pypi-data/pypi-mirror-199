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


def test_order_item_add():
	"""
	Tests the OrderItem_Add API Call
	"""

	helper.provision_store('OrderItem_Add.xml')

	order_item_add_test_insertion()
	order_item_add_test_add_product()
	order_item_add_test_add_product_with_option()
	order_item_add_test_insertion_with_attribute()
	order_item_add_test_insertion_with_invalid_attribute()


def order_item_add_test_insertion():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678565)\
		.set_code('OrderItemAddTest_Foo')\
		.set_quantity(2)\
		.set_price(10.00)\
		.set_taxable(True)\
		.set_weight(1.00)\
		.set_sku('OrderItemAddTest_Foo_SKU')\
		.set_name('OrderItemAddTest - Foo')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 20.00
	assert response.get_order_total_and_item().get_formatted_total() == '$20.00'
	assert response.get_order_total_and_item().get_order_item() is not None
	assert response.get_order_total_and_item().get_order_item().get_code() == 'OrderItemAddTest_Foo'
	assert response.get_order_total_and_item().get_order_item().get_quantity() == 2
	assert response.get_order_total_and_item().get_order_item().get_price() == 10.00
	assert response.get_order_total_and_item().get_order_item().get_weight() == 1.00
	assert response.get_order_total_and_item().get_order_item().get_sku() == 'OrderItemAddTest_Foo_SKU'
	assert response.get_order_total_and_item().get_order_item().get_name() == 'OrderItemAddTest - Foo'

	order = helper.get_order(678565)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item = order.get_items()[0]

	assert isinstance(item, merchantapi.model.OrderItem)
	assert item.get_line_id() == response.get_order_total_and_item().get_order_item().get_line_id()


def order_item_add_test_add_product():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678566) \
		.set_code('OrderItemAddTest_Product') \
		.set_quantity(1) \
		.set_price(9.99) \
		.set_name('OrderItemAddTest_Product')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 9.99
	assert response.get_order_total_and_item().get_formatted_total() == '$9.99'

	order = helper.get_order(678566)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 1

	item = order.get_items()[0]

	assert isinstance(item, merchantapi.model.OrderItem)
	assert item.get_code() == 'OrderItemAddTest_Product'
	assert item.get_quantity() == 1
	assert item.get_name() == 'OrderItemAddTest_Product'


def order_item_add_test_add_product_with_option():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678567) \
		.set_code('OrderItemAddTest_Product_2') \
		.set_quantity(1) \
		.set_price(12.99) \
		.set_name('OrderItemAddTest_Product_2')

	option = merchantapi.model.OrderItemOption()

	option.set_attribute_code('color')\
		.set_value('red')

	request.add_option(option)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 12.99
	assert response.get_order_total_and_item().get_formatted_total() == '$12.99'


def order_item_add_test_insertion_with_attribute():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678568) \
		.set_code('OrderItemAddTest_ItemWOptions') \
		.set_quantity(1) \
		.set_price(12.99) \
		.set_name('OrderItemAddTest_ItemWOptions')

	option = merchantapi.model.OrderItemOption()

	option.set_attribute_code('foo')\
		.set_value('bar')\
		.set_price(3.29)\
		.set_weight(1.25)

	request.add_option(option)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_total() == 16.28
	assert response.get_order_total_and_item().get_formatted_total() == '$16.28'


def order_item_add_test_insertion_with_invalid_attribute():
	request = merchantapi.request.OrderItemAdd(helper.init_client())

	request.set_order_id(678568) \
		.set_code('OrderItemAddTest_ItemWOptions') \
		.set_quantity(1) \
		.set_price(12.99) \
		.set_name('OrderItemAddTest_ItemWOptions')

	option = merchantapi.model.OrderItemOption()

	option.set_attribute_code('')\
		.set_value('')

	request.add_option(option)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderItemAdd)
