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


def test_customer_address_insert():
	"""
	Tests the CustomerAddress_Insert API Call
	"""

	helper.provision_store('CustomerAddress_Insert.xml')

	customer_address_insert_test_insertion()


def customer_address_insert_test_insertion():
	customer = helper.get_customer('CustomerAddressInsertTest')
	addresses = helper.get_customer_addresses('CustomerAddressInsertTest')

	assert customer is not None
	assert addresses is not None
	assert len(addresses) >= 1

	request = merchantapi.request.CustomerAddressInsert(helper.init_client(), customer)

	request.set_description('CustomerAddressInsertTest')
	request.set_first_name('Insert')
	request.set_last_name('Test')
	request.set_email('test@coolcommerce.net')
	request.set_phone('1231231234')
	request.set_fax('3213214321')
	request.set_company('Miva Inc')
	request.set_address1('1234 Miva St')
	request.set_address2('Ste 1')
	request.set_city('San Diego')
	request.set_state('CA')
	request.set_zip('92009')
	request.set_country('US')
	request.set_residential(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressInsert)

	assert isinstance(response.get_customer_address(), merchantapi.model.CustomerAddress)
	assert response.get_customer_address().get_description() == 'CustomerAddressInsertTest'
	assert response.get_customer_address().get_first_name() == 'Insert'
	assert response.get_customer_address().get_last_name() == 'Test'
	assert response.get_customer_address().get_email() == 'test@coolcommerce.net'
	assert response.get_customer_address().get_phone() == '1231231234'
	assert response.get_customer_address().get_fax() == '3213214321'
	assert response.get_customer_address().get_company() == 'Miva Inc'
	assert response.get_customer_address().get_address1() == '1234 Miva St'
	assert response.get_customer_address().get_address2() == 'Ste 1'
	assert response.get_customer_address().get_city() == 'San Diego'
	assert response.get_customer_address().get_state() == 'CA'
	assert response.get_customer_address().get_zip() == '92009'
	assert response.get_customer_address().get_country() == 'US'
	assert response.get_customer_address().get_residential() is True

	address = None
	for a in helper.get_customer_addresses('CustomerAddressInsertTest'):
		if a.get_description() == 'CustomerAddressInsertTest':
			address = a
			break

	assert address is not None
	assert address.get_id() == response.get_customer_address().get_id()
