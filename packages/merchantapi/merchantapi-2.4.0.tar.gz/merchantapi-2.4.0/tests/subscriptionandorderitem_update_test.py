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


def test_subscription_and_order_item_update():
	"""
	Tests the SubscriptionAndOrderItem_Update API Call
	"""

	helper.provision_store('SubscriptionAndOrderItem_Update.xml')

	subscription_and_order_item_update_test_update()


def subscription_and_order_item_update_test_update():
	customer = helper.get_customer('SubscriptionAndOrderItem_Update_1')
	addresses = helper.get_customer_addresses('SubscriptionAndOrderItem_Update_1')
	product = helper.get_product('SubscriptionAndOrderItem_Update_1')
	order = helper.get_order(678568)

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1
	assert order is not None

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionAndOrderItem_Update')

	assert methods is not None
	assert len(methods) is 1

	create_request = merchantapi.request.SubscriptionAndOrderItemAdd(helper.init_client())

	create_request.set_product_code(product.get_code())
	create_request.set_customer_id(customer.get_id())
	create_request.set_customer_address_id(addresses[0].get_id())
	create_request.set_payment_card_id(payment_card.get_id())
	create_request.set_product_subscription_term_description('Daily')
	create_request.set_ship_id(methods[0].get_module().get_id())
	create_request.set_ship_data('SubscriptionAndOrderItem_Add')
	create_request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	create_request.set_quantity(1)
	create_request.set_order_id(order.get_id())

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('red')

	create_request.add_attribute(attr1)

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.SubscriptionAndOrderItemAdd)

	load = helper.get_order(order.get_id())

	assert load is not None
	assert load.get_items()[0].get_subscription_id() > 0

	payment_card_change = helper.register_payment_card_with_address(customer, addresses[1])

	assert payment_card_change is not None

	request = merchantapi.request.SubscriptionAndOrderItemUpdate(helper.init_client())

	request.set_order_id(load.get_id());
	request.set_line_id(load.get_items()[0].get_line_id())
	request.set_subscription_id(load.get_items()[0].get_subscription_id())
	request.set_payment_card_id(payment_card_change.get_id())
	request.set_quantity(1)
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))

	attr1change = merchantapi.model.SubscriptionAttribute()

	attr1change.set_code('color')
	attr1change.set_value('green')

	request.add_attribute(attr1change)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionAndOrderItemUpdate)

	check = helper.get_subscription(customer.get_id(), load.get_items()[0].get_subscription_id())

	assert check is not None

	assert check.get_customer_payment_card_id() == payment_card_change.get_id()
	assert check.get_options() is not None and len(check.get_options()) == 1
	assert check.get_options()[0].get_value() == 'green'
