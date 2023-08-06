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


def test_customer_delete():
	"""
	Tests the Customer_Delete API Call
	"""

	helper.provision_store('Customer_Delete.xml')

	customer_delete_test_deletion()
	customer_delete_test_invalid_customer()


def customer_delete_test_deletion():
	request = merchantapi.request.CustomerDelete(helper.init_client())

	request.set_edit_customer('CustomerDeleteTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerDelete)

	customer = helper.get_customer('CustomerDeleteTest')

	assert customer is None


def customer_delete_test_invalid_customer():
	request = merchantapi.request.CustomerDelete(helper.init_client())

	request.set_edit_customer('InvalidCustomerLogin')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CustomerDelete)
