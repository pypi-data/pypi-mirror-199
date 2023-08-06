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


def test_customer_address_list_load_query():
	"""
	Tests the CustomerAddressList_Load_Query API Call
	"""

	helper.provision_store('CustomerAddressList_Load_Query.xml')

	customer_address_list_load_query_test_list_load()
	customer_address_list_load_query_test_list_load_filtered()


def customer_address_list_load_query_test_list_load():
	customer = helper.get_customer('CustomerAddressListLoadQueryTest')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_login() == 'CustomerAddressListLoadQueryTest'
	assert customer.get_id() > 0

	request = merchantapi.request.CustomerAddressListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerAddressListLoadQueryTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressListLoadQuery)

	assert isinstance(response.get_customer_addresses(), list)
	assert len(response.get_customer_addresses()) == 3

	for i, address in enumerate(response.get_customer_addresses()):
		assert isinstance(address, merchantapi.model.CustomerAddress)
		assert address.get_customer_id() == customer.get_id()


def customer_address_list_load_query_test_list_load_filtered():
	customer = helper.get_customer('CustomerAddressListLoadQueryTest')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_login() == 'CustomerAddressListLoadQueryTest'
	assert customer.get_id() > 0

	request = merchantapi.request.CustomerAddressListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerAddressListLoadQueryTest')
	request.set_filters(request.filter_expression().equal('fname', 'Joe'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressListLoadQuery)

	assert isinstance(response.get_customer_addresses(), list)
	assert len(response.get_customer_addresses()) == 1

	for i, address in enumerate(response.get_customer_addresses()):
		assert isinstance(address, merchantapi.model.CustomerAddress)
		assert address.get_customer_id() == customer.get_id()
		assert address.get_first_name() == 'Joe'
