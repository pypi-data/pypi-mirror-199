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


def test_business_account_customer_update_assigned():
	"""
	Tests the BusinessAccountCustomer_Update_Assigned API Call
	"""

	helper.provision_store('BusinessAccountCustomer_Update_Assigned.xml')

	business_account_customer_update_assigned_test_assignment()
	business_account_customer_update_assigned_test_unassignment()


def business_account_customer_update_assigned_test_assignment():
	request = merchantapi.request.BusinessAccountCustomerUpdateAssigned(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerUpdateAssignedTest_1')
	request.set_customer_login('BusinessAccountCustomerUpdateAssignedTest_2')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerUpdateAssigned)

	check = helper.get_customer_business_account('BusinessAccountCustomerUpdateAssignedTest_1', 'BusinessAccountCustomerUpdateAssignedTest_2', True, False)
	assert len(check) == 1


def business_account_customer_update_assigned_test_unassignment():
	request = merchantapi.request.BusinessAccountCustomerUpdateAssigned(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerUpdateAssignedTest_1')
	request.set_customer_login('BusinessAccountCustomerUpdateAssignedTest_1')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerUpdateAssigned)

	check = helper.get_customer_business_account('BusinessAccountCustomerUpdateAssignedTest_1', 'BusinessAccountCustomerUpdateAssignedTest_1', False, True)
	assert len(check) == 1
