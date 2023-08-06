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


def test_subscription_insert():
	"""
	Tests the Subscription_Insert API Call
	"""

	helper.provision_store('Subscription_Insert.xml')

	subscription_insert_test_insert()
	subscription_insert_test_insert_with_attribute()


def subscription_insert_test_insert():
	customer = helper.get_customer('Subscription_Insert_1')
	addresses = helper.get_customer_addresses('Subscription_Insert_1')
	product = helper.get_product('Subscription_Insert_1')

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'Subscription_Insert')

	assert methods is not None
	assert len(methods) is 1

	request = merchantapi.request.SubscriptionInsert(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('Subscription_Insert')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionInsert)

	assert response.get_subscription() is not None
	assert response.get_subscription().get_id() > 0


def subscription_insert_test_insert_with_attribute():
	customer = helper.get_customer('Subscription_Insert_2')
	addresses = helper.get_customer_addresses('Subscription_Insert_2')
	product = helper.get_product('Subscription_Insert_2')

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) >= 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'Subscription_Insert')

	assert methods is not None
	assert len(methods) is 1

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('green')

	request = merchantapi.request.SubscriptionInsert(helper.init_client())

	request.set_product_code(product.get_code())
	request.set_customer_id(customer.get_id())
	request.set_customer_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_product_subscription_term_description('Daily')
	request.set_ship_id(methods[0].get_module().get_id())
	request.set_ship_data('Subscription_Insert')
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))
	request.set_quantity(1)
	request.add_attribute(attr1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionInsert)

	assert response.get_subscription() is not None
	assert response.get_subscription().get_id() > 0
	assert len(response.get_subscription().get_options()) == 1
	assert response.get_subscription().get_options()[0].get_value() == "green"
