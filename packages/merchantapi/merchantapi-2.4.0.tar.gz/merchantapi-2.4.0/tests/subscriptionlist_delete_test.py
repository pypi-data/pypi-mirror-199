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


def test_subscription_list_delete():
	"""
	Tests the SubscriptionList_Delete API Call
	"""

	helper.provision_store('SubscriptionList_Delete.xml')

	subscription_list_delete_test_deletion()


def subscription_list_delete_test_deletion():
	customer = helper.get_customer('SubscriptionList_Delete_1')
	addresses = helper.get_customer_addresses('SubscriptionList_Delete_1')
	products = helper.get_products(['SubscriptionList_Delete_1', 'SubscriptionList_Delete_2', 'SubscriptionList_Delete_3'])

	assert customer is not None
	assert products is not None
	assert len(products) == 3
	assert addresses is not None
	assert len(addresses) >= 1

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], payment_card, 1, 'CO', 'SubscriptionList_Delete')

	assert methods is not None
	assert len(methods) is 1

	subscription1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'SubscriptionList_Delete', 1, [])
	subscription2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'SubscriptionList_Delete', 1, [])
	subscription3 = helper.create_subscription(customer, products[2], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], payment_card, methods[0].get_module().get_id(), 'SubscriptionList_Delete', 1, [])

	assert subscription1 is not None
	assert subscription2 is not None
	assert subscription3 is not None

	request = merchantapi.request.SubscriptionListDelete(helper.init_client())

	request.add_subscription(subscription1)
	request.add_subscription(subscription2)
	request.add_subscription(subscription3)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionListDelete)

	check_request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())
	check_request.set_customer_id(customer.get_id())
	check_request.filters.is_in('id', ','.join([str(subscription1.get_id()), str(subscription2.get_id()), str(subscription3.get_id())]))

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(check_response.get_customer_subscriptions()) == 0
