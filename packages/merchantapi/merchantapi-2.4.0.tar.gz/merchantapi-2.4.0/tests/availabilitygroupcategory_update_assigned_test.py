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


def test_availability_group_category_update_assigned():
	"""
	Tests the AvailabilityGroupCategory_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupCategory_Update_Assigned.xml')

	availability_group_category_update_assigned_test_assignment()
	availability_group_category_update_assigned_test_unassignment()


def availability_group_category_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupCategoryUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCatUpdateAssignedTest')
	request.set_category_code('AvailabilityGrpCatUpdateAssignedTest_Cat2')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryUpdateAssigned)

	check = helper.get_availability_group_categories('AvailabilityGrpCatUpdateAssignedTest', 'AvailabilityGrpCatUpdateAssignedTest_Cat2', True, False)

	assert len(check) == 1


def availability_group_category_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupCategoryUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpCatUpdateAssignedTest')
	request.set_category_code('AvailabilityGrpCatUpdateAssignedTest_Cat1')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryUpdateAssigned)

	check = helper.get_availability_group_categories('AvailabilityGrpCatUpdateAssignedTest', 'AvailabilityGrpCatUpdateAssignedTest_Cat1', False, True)

	assert len(check) == 1
