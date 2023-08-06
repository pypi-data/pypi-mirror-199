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


def test_availability_group_product_update_assigned():
	"""
	Tests the AvailabilityGroupProduct_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupProduct_Update_Assigned.xml')

	availability_group_product_update_assigned_test_assignment()
	availability_group_product_update_assigned_test_unassignment()
	availability_group_product_update_assigned_test_invalid_assign()
	availability_group_product_update_assigned_test_invalid_availability_group()
	availability_group_product_update_assigned_test_invalid_product()


def availability_group_product_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_product_code('AvailabilityGrpProdUpdateAssignedTest_Product')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)


def availability_group_product_update_assigned_test_invalid_product():
	request = merchantapi.request.AvailabilityGroupProductUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpProdUpdateAssignedTest')\
		.set_product_code('InvalidProduct')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupProductUpdateAssigned)