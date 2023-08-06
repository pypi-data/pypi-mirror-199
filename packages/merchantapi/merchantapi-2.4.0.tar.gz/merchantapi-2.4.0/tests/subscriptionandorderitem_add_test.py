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
import datetime
from . import helper


def test_subscription_and_order_item_add():
	"""
	Tests the SubscriptionAndOrderItem_Add API Call
	"""

	helper.provision_store('SubscriptionAndOrderItem_Add.xml')

	subscription_and_order_item_add_test_add()
	subscription_and_order_item_add_test_add_with_attribute()


def subscription_and_order_item_add_test_add():
	customer = helper.get_customer('SubscriptionAndOrderItem_Add_1')
	addresses = helper.get_customer_addresses('SubscriptionAndOrderItem_Add_1')
	product = helper.get_product('SubscriptionAndOrderItem_Add_1')
	order = helper.get_order(678568)

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1
	assert order is not None

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionAndOrderItem_Add')

	assert methods is not None
	assert len(methods) is 1

	request = merchantapi.request.SubscriptionAndOrderItemAdd(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('SubscriptionAndOrderItem_Add')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)
	request.set_order_id(order.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionAndOrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_order_item() is not None
	assert response.get_order_total_and_item().get_order_item().get_subscription_id() > 0

	check = helper.get_order(order.get_id())

	assert check is not None
	assert check.get_items()[0].get_subscription_id() > 0


def subscription_and_order_item_add_test_add_with_attribute():
	customer = helper.get_customer('SubscriptionAndOrderItem_Add_2')
	addresses = helper.get_customer_addresses('SubscriptionAndOrderItem_Add_2')
	product = helper.get_product('SubscriptionAndOrderItem_Add_2')
	order = helper.get_order(678569)

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1
	assert order is not None

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionAndOrderItem_Add')

	assert methods is not None
	assert len(methods) is 1

	request = merchantapi.request.SubscriptionAndOrderItemAdd(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('SubscriptionAndOrderItem_Add')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)
	request.set_order_id(order.get_id())

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('green')

	request.add_attribute(attr1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionAndOrderItemAdd)

	assert isinstance(response.get_order_total_and_item(), merchantapi.model.OrderTotalAndItem)
	assert response.get_order_total_and_item().get_order_item() is not None
	assert response.get_order_total_and_item().get_order_item().get_subscription_id() > 0

	check = helper.get_order(order.get_id())

	assert check is not None
	assert check.get_items()[0].get_subscription_id() > 0
	assert check.get_items()[0].get_subscription().get_options()[0].get_value() == 'green'
