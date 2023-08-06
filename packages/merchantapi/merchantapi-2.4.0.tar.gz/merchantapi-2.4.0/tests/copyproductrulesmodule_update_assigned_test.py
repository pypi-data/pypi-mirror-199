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


def test_copyproductrulesmodule_update_assigned():
	"""
	Tests the CopyProductRulesModule_Update_Assigned API Call
	"""

	helper.provision_store('CopyProductRulesModule_Update_Assigned.xml')

	copyproductrulesmodule_update_assigned_test_assignment()
	copyproductrulesmodule_update_assigned_test_unassignment()


def copyproductrulesmodule_update_assigned_test_assignment():
	request = merchantapi.request.CopyProductRulesModuleUpdateAssigned(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesModule_Update_Assigned_1')
	request.set_module_code('customfields')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesModuleUpdateAssigned)
	
	check = get_copy_product_rules_module_code('CopyProductRulesModule_Update_Assigned_1', 'Custom Fields')
	assert check is not None
	assert check.get_assigned() is True


def copyproductrulesmodule_update_assigned_test_unassignment():
	request = merchantapi.request.CopyProductRulesModuleUpdateAssigned(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesModule_Update_Assigned_1')
	request.set_module_code('combofacets')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesModuleUpdateAssigned)

	check = get_copy_product_rules_module_code('CopyProductRulesModule_Update_Assigned_1', 'Combination Facets')
	assert check is not None
	assert check.get_assigned() is False


def get_copy_product_rules_module_code(name: str, module_name: str):
	request = merchantapi.request.CopyProductRulesModuleListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name(name)
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().equal('module_name', module_name)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesModuleListLoadQuery)

	return response.get_copy_product_rules_modules()[0] if len(response.get_copy_product_rules_modules()) else None