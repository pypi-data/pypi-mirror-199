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


def test_customer_subscription_list_load_query():
	"""
	Tests the CustomerSubscriptionList_Load_Query API Call
	"""

	helper.provision_store('CustomerSubscriptionList_Load_Query.xml')

	customer_subscription_list_load_query_test_list_load()
	customer_subscription_list_load_query_test_list_load_with_filters()


def customer_subscription_list_load_query_test_list_load():
	customer = helper.get_customer('CSLLQ_1')
	products = helper.get_products(['CSLLQ_1', 'CSLLQ_2'])
	addresses = helper.get_customer_addresses('CSLLQ_1')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'CSLLQ')

	assert methods is not None and len(methods) == 1

	sub1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)
	sub2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)

	request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())

	request.set_customer_id(customer.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(response.get_customer_subscriptions()) == 2

	for sub in response.get_customer_subscriptions():
		assert sub.get_id() == sub1.get_id() or sub.get_id() == sub2.get_id()


def customer_subscription_list_load_query_test_list_load_with_filters():
	customer = helper.get_customer('CSLLQ_2')
	products = helper.get_products(['CSLLQ_1', 'CSLLQ_2'])
	addresses = helper.get_customer_addresses('CSLLQ_2')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'CSLLQ');

	assert methods is not None and len(methods) == 1

	sub1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)
	sub2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)

	request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())

	request.set_customer_id(customer.get_id())
	request.filters.equal('product_code', products[1].get_code())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(response.get_customer_subscriptions()) == 1
	assert response.get_customer_subscriptions()[0].get_id() == sub2.get_id()
