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


def test_availability_group_shipping_method_update_assigned():
	"""
	Tests the AvailabilityGroupShippingMethod_Update_Assigned API Call
	"""

	helper.provision_store('AvailabilityGroupShippingMethod_Update_Assigned.xml')

	availability_group_shipping_method_update_assigned_test_assignment()
	availability_group_shipping_method_update_assigned_test_unassignment()
	availability_group_shipping_method_update_assigned_test_invalid_assign()
	availability_group_shipping_method_update_assigned_test_invalid_availability_group()


def availability_group_shipping_method_update_assigned_test_assignment():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpShpMethUpdateAssignedTest')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def availability_group_shipping_method_update_assigned_test_unassignment():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('AvailabilityGrpShpMethUpdateAssignedTest')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def availability_group_shipping_method_update_assigned_test_invalid_assign():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_availability_group_name('AvailabilityGrpShpMethUpdateAssignedTest')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)


def availability_group_shipping_method_update_assigned_test_invalid_availability_group():
	request = merchantapi.request.AvailabilityGroupShippingMethodUpdateAssigned(helper.init_client())

	request.set_availability_group_name('InvalidAvailabilityGroup')\
		.set_module_code('flatrate')\
		.set_method_code('AvailabilityGrpShpMethUpdateAssignedTest_Method')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.AvailabilityGroupShippingMethodUpdateAssigned)
