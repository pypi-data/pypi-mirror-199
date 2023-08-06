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


def test_availability_group_business_account_update_assigned():
	"""
	Tests the AvailabilityGroupBusinessAccount_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupBusinessAccount_Update_Assigned.xml')

	availability_group_business_account_update_assigned_test_assignment()
	availability_group_business_account_update_assigned_test_unassignment()
	availability_group_business_account_update_assigned_test_invalid_assign()
	availability_group_business_account_update_assigned_test_invalid_availability_group()
	availability_group_business_account_update_assigned_test_invalid_business_account()


def availability_group_business_account_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_business_account_title('AvailabilityGrpBusAccUpdateAssignedTest_BusinessAccount')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)


def availability_group_business_account_update_assigned_test_invalid_business_account():
	request = merchantapi.request.AvailabilityGroupBusinessAccountUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpBusAccUpdateAssignedTest')\
		.set_business_account_title('InvalidBusinessAccount')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned)
