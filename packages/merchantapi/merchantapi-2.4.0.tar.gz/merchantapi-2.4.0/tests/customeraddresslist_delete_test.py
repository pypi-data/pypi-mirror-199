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


def test_customer_address_list_delete():
	"""
	Tests the CustomerAddressList_Delete API Call
	"""

	helper.provision_store('CustomerAddressList_Delete.xml')

	customer_address_list_delete_test_deletion()


def customer_address_list_delete_test_deletion():
	addresses = helper.get_customer_addresses('CustomerAddressListDeleteTest')
	assert addresses is not None
	assert len(addresses) >= 3

	request = merchantapi.request.CustomerAddressListDelete(helper.init_client())

	request.set_customer_login('CustomerAddressListDeleteTest')

	for a in addresses:
		request.add_customer_address(a)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerAddressListDelete)

	check = helper.get_customer_addresses('CustomerAddressListDeleteTest')

	assert len(check) == 0
