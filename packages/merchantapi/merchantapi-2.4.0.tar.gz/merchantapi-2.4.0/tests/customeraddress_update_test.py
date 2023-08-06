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


def test_customer_address_update():
	"""
	Tests the CustomerAddress_Update API Call
	"""

	helper.provision_store('CustomerAddress_Update.xml')

	customer_address_update_test_update()


def customer_address_update_test_update():
	address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateTest'):
		if a.get_description() == 'CustomerAddressUpdateTest_Addr1':
			address = a
			break

	assert address is not None

	request = merchantapi.request.CustomerAddressUpdate(helper.init_client(), address)

	request.set_description(address.get_description() + ' UPDATED')
	request.set_first_name(address.get_first_name() + ' UPDATED')
	request.set_last_name(address.get_last_name() + ' UPDATED')
	request.set_email(address.get_email() + '.up')
	request.set_phone(address.get_phone() + '1')
	request.set_fax(address.get_fax() + '1')
	request.set_company(address.get_company() + ' UPDATED')
	request.set_address1(address.get_address1() + ' UPDATED')
	request.set_address2(address.get_address2() + ' UPDATED')
	request.set_city(address.get_city() + ' UPDATED')
	request.set_state(address.get_state() + ' UPDATED')
	request.set_zip(address.get_zip() + ' UPDATED')
	request.set_country(address.get_country() + ' UPDATED')
	request.set_residential(not address.get_residential())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressUpdate)

	check_address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateTest'):
		if a.get_id() == address.get_id():
			check_address = a
			break

	assert check_address is not None
	assert address.get_description() != check_address.get_description()
	assert address.get_first_name() != check_address.get_first_name()
	assert address.get_last_name() != check_address.get_last_name()
	assert address.get_email() != check_address.get_email()
	assert address.get_phone() != check_address.get_phone()
	assert address.get_fax() != check_address.get_fax()
	assert address.get_company() != check_address.get_company()
	assert address.get_address1() != check_address.get_address1()
	assert address.get_address2() != check_address.get_address2()
	assert address.get_city() != check_address.get_city()
	assert address.get_state() != check_address.get_state()
	assert address.get_zip() != check_address.get_zip()
	assert address.get_country() != check_address.get_country()
	assert address.get_residential() != check_address.get_residential()
	