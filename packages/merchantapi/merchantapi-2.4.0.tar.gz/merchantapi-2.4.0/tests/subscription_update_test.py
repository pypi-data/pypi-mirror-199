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


def test_subscription_update():
	"""
	Tests the Subscription_Update API Call
	"""

	helper.provision_store('Subscription_Update.xml')

	subscription_update_test_update()


def subscription_update_test_update():
	customer = helper.get_customer('Subscription_Update_1')
	addresses = helper.get_customer_addresses('Subscription_Update_1')
	product = helper.get_product('Subscription_Update_1')

	assert customer is not None
	assert product is not None
	assert addresses is not None
	assert len(addresses) > 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, product, 'Daily', addresses[0], payment_card, 1, 'CO', 'Subscription_Update')

	assert methods is not None
	assert len(methods) is 1

	attr1 = merchantapi.model.SubscriptionAttribute()

	attr1.set_code('color')
	attr1.set_value('red')

	subscription = helper.create_subscription(customer, product, 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'Subscription_Update', 1, [ attr1 ])

	assert subscription is not None

	payment_card_change = helper.register_payment_card_with_address(customer, addresses[1])

	assert payment_card_change is not None

	request = merchantapi.request.SubscriptionUpdate(helper.init_client())

	request.set_subscription_id(subscription.get_id())
	request.set_payment_card_id(payment_card_change.get_id())
	request.set_quantity(1)
	request.set_next_date(int(time.mktime(datetime.date.today().timetuple())))

	attr1change = merchantapi.model.SubscriptionAttribute()

	attr1change.set_code('color')
	attr1change.set_value('green')

	request.add_attribute(attr1change)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionUpdate)

	check = helper.get_subscription(customer.get_id(), subscription.get_id())

	assert check is not None

	assert check.get_customer_payment_card_id() == payment_card_change.get_id()
	assert len(check.get_options()) is 1
	assert check.get_options()[0].get_value() == 'green'
