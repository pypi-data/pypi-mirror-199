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


def test_copypageruleslist_delete():
	"""
	Tests the CopyPageRulesList_Delete API Call
	"""

	helper.provision_store('CopyPageRulesList_Delete.xml')

	copypageruleslist_delete_test_deletion()


def copypageruleslist_delete_test_deletion():
	load_request = merchantapi.request.CopyPageRulesListLoadQuery(helper.init_client())
	load_request.get_filters().is_in('name', [ 'CopyPageRulesList_Delete_1', 'CopyPageRulesList_Delete_2', 'CopyPageRulesList_Delete_3' ])
	load_response = load_request.send()
	helper.validate_response_success(load_response, merchantapi.response.CopyPageRulesListLoadQuery)

	assert len(load_response.get_copy_page_rules()) == 3

	request = merchantapi.request.CopyPageRulesListDelete(helper.init_client())

	request.add_copy_page_rule(load_response.get_copy_page_rules()[0])
	request.add_copy_page_rule(load_response.get_copy_page_rules()[1])
	request.add_copy_page_rule(load_response.get_copy_page_rules()[2])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesListDelete)

	load_response = load_request.send()
	helper.validate_response_success(load_response, merchantapi.response.CopyPageRulesListLoadQuery)
	assert len(load_response.get_copy_page_rules()) == 0
