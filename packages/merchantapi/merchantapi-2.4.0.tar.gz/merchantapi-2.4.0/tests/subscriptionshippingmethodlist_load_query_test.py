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


def test_subscription_shipping_method_list_load_query():
	"""
	Tests the SubscriptionShippingMethodList_Load_Query API Call
	"""

	helper.provision_store('SubscriptionShippingMethodList_Load_Query.xml')

	subscription_shipping_method_list_load_query_test_list_load()


def subscription_shipping_method_list_load_query_test_list_load():
	customer = helper.get_customer('SSMLLQ_1')
	product = helper.get_product('SSMLLQ_1')

	assert customer is not None
	assert product is not None

	addresses = helper.get_customer_addresses(customer.get_login())

	assert addresses is not None
	assert len(addresses) > 0

	payment_card = helper.register_payment_card_with_address(customer, addresses[0])

	assert payment_card is not None

	request = merchantapi.request.SubscriptionShippingMethodListLoadQuery(helper.init_client())

	request.set_product_id(product.get_id())
	request.set_customer_id(customer.get_id())
	request.set_address_id(addresses[0].get_id())
	request.set_payment_card_id(payment_card.get_id())
	request.set_quantity(1)
	request.set_product_subscription_term_description('Daily')

	request.filters.contains('method', 'SSMLLQ_')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.SubscriptionShippingMethodListLoadQuery)

	assert len(response.get_subscription_shipping_methods()) is 3
	for method in response.get_subscription_shipping_methods():
		assert method.get_module() is not None
		assert method.get_module().get_id() > 0
		assert 'SSMLLQ_' in method.get_method_name()
