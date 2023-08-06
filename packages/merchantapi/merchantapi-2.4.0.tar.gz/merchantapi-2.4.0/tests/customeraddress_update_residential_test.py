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


def test_customer_address_update_residential():
	"""
	Tests the CustomerAddress_Update_Residential API Call
	"""

	helper.provision_store('CustomerAddress_Update_Residential.xml')

	customer_address_update_residential_test_update()


def customer_address_update_residential_test_update():
	address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateResidentialTest'):
		if a.get_description() == 'CustomerAddressUpdateResidentialTest_Addr1':
			address = a
			break

	assert address is not None

	request = merchantapi.request.CustomerAddressUpdateResidential(helper.init_client())

	request.set_customer_address_id(address.get_id())
	request.set_residential(not address.get_residential())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressUpdateResidential)

	check_address = None
	for a in helper.get_customer_addresses('CustomerAddressUpdateResidentialTest'):
		if a.get_id() == address.get_id():
			check_address = a
			break

	assert check_address is not None
	assert check_address.get_residential() != address.get_residential()
