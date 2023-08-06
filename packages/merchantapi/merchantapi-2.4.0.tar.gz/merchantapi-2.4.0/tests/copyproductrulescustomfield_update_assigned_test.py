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


def test_copyproductrulescustom_field_update_assigned():
	"""
	Tests the CopyProductRulesCustomField_Update_Assigned API Call
	"""

	helper.provision_store('CopyProductRulesCustomField_Update_Assigned.xml')

	copyproductrulescustom_field_update_assigned_test_assignment()
	copyproductrulescustom_field_update_assigned_test_unassignment()


def copyproductrulescustom_field_update_assigned_test_assignment():
	request = merchantapi.request.CopyProductRulesCustomFieldUpdateAssigned(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesCustomField_Update_Assigned_1')
	request.set_module_code('customfields')
	request.set_field_code('CopyProductRulesCustomField_Update_Assigned_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesCustomFieldUpdateAssigned)
	
	check = get_copy_product_rules_custom_field_code('CopyProductRulesCustomField_Update_Assigned_1', 'CopyProductRulesCustomField_Update_Assigned_1')
	assert check is not None
	assert check.get_assigned() is True


def copyproductrulescustom_field_update_assigned_test_unassignment():
	request = merchantapi.request.CopyProductRulesCustomFieldUpdateAssigned(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesCustomField_Update_Assigned_1')
	request.set_module_code('customfields')
	request.set_field_code('CopyProductRulesCustomField_Update_Assigned_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesCustomFieldUpdateAssigned)

	check = get_copy_product_rules_custom_field_code('CopyProductRulesCustomField_Update_Assigned_1', 'CopyProductRulesCustomField_Update_Assigned_2')
	assert check is not None
	assert check.get_assigned() is False


def get_copy_product_rules_custom_field_code(name: str, field_code: str):
	request = merchantapi.request.CopyProductRulesCustomFieldListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name(name)
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().equal('field_code', field_code)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesCustomFieldListLoadQuery)

	return response.get_copy_product_rules_custom_fields()[0] if len(response.get_copy_product_rules_custom_fields()) else None