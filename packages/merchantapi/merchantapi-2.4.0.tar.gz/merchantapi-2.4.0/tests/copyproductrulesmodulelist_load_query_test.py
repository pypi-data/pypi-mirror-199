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


def test_copyproductrulesmodulelist_load_query():
	"""
	Tests the CopyProductRulesModuleList_Load_Query API Call
	"""

	helper.provision_store('CopyProductRulesModuleList_Load_Query.xml')

	copyproductrulesmodulelist_load_query_test_list_load_all()
	copyproductrulesmodulelist_load_query_test_list_load_assigned()
	copyproductrulesmodulelist_load_query_test_list_load_unassigned()


def copyproductrulesmodulelist_load_query_test_list_load_all():
	request = merchantapi.request.CopyProductRulesModuleListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesModuleList_Load_Query_1')
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().is_in('module_name', [ 'Combination Facets', 'Custom Fields' ])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesModuleListLoadQuery)

	assert len(response.get_copy_product_rules_modules()) == 2


def copyproductrulesmodulelist_load_query_test_list_load_assigned():
	request = merchantapi.request.CopyProductRulesModuleListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesModuleList_Load_Query_1')
	request.set_assigned(True)
	request.set_unassigned(False)
	request.get_filters().is_in('module_name', [ 'Combination Facets', 'Custom Fields' ])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesModuleListLoadQuery)

	assert len(response.get_copy_product_rules_modules()) == 1


def copyproductrulesmodulelist_load_query_test_list_load_unassigned():
	request = merchantapi.request.CopyProductRulesModuleListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesModuleList_Load_Query_1')
	request.set_assigned(False)
	request.set_unassigned(True)
	request.get_filters().is_in('module_name', [ 'Combination Facets', 'Custom Fields' ])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesModuleListLoadQuery)

	assert len(response.get_copy_product_rules_modules()) == 1