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


def test_copyproductruleslist_delete():
	"""
	Tests the CopyProductRulesList_Delete API Call
	"""

	helper.provision_store('CopyProductRulesList_Delete.xml')

	copyproductruleslist_delete_test_deletion()


def copyproductruleslist_delete_test_deletion():
	load_request = merchantapi.request.CopyProductRulesListLoadQuery(helper.init_client())
	load_request.get_filters().is_in('name', [ 'CopyProductRulesList_Delete_1', 'CopyProductRulesList_Delete_2', 'CopyProductRulesList_Delete_3' ])
	load_response = load_request.send()
	helper.validate_response_success(load_response, merchantapi.response.CopyProductRulesListLoadQuery)

	assert len(load_response.get_copy_product_rules()) == 3

	request = merchantapi.request.CopyProductRulesListDelete(helper.init_client())

	request.add_copy_product_rule(load_response.get_copy_product_rules()[0])
	request.add_copy_product_rule(load_response.get_copy_product_rules()[1])
	request.add_copy_product_rule(load_response.get_copy_product_rules()[2])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesListDelete)

	load_response = load_request.send()
	helper.validate_response_success(load_response, merchantapi.response.CopyProductRulesListLoadQuery)
	assert len(load_response.get_copy_product_rules()) == 0