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


def test_customer_address_delete():
	"""
	Tests the CustomerAddress_Delete API Call
	"""

	helper.provision_store('CustomerAddress_Delete.xml')

	customer_address_delete_test_deletion()


def customer_address_delete_test_deletion():
	address = None
	for a in helper.get_customer_addresses('CustomerAddressDeleteTest'):
		if a.get_description() == 'CustomerAddressDeleteTest_Addr1':
			address = a
			break

	assert address is not None

	request = merchantapi.request.CustomerAddressDelete(helper.init_client())

	request.set_customer_login('CustomerAddressDeleteTest')
	request.set_customer_address_id(address.get_id())
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressDelete)

	check = None
	for a in helper.get_customer_addresses('CustomerAddressDeleteTest'):
		if a.get_id() == address.get_id():
			check = a
			break

	assert check is None
