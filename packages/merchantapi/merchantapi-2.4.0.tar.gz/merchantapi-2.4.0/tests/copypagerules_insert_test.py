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


def test_copypagerules_insert():
	"""
	Tests the CopyPageRules_Insert API Call
	"""

	helper.provision_store('CopyPageRules_Insert.xml')

	copypagerules_insert_test_insertion()


def copypagerules_insert_test_insertion():
	request = merchantapi.request.CopyPageRulesInsert(helper.init_client())

	request.set_name('CopyPageRules_Insert_1')
	request.set_secure(True)
	request.set_title(False)
	request.set_template(True)
	request.set_items(True)
	request.set_javascript_resource_assignments(True)
	request.set_cache_settings(True)
	request.set_settings(merchantapi.model.CopyPageRule.PAGE_RULE_SETTINGS_ALL)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesInsert)

	assert response.get_copy_page_rule() is not None
	assert response.get_copy_page_rule().get_name() == 'CopyPageRules_Insert_1'
	assert response.get_copy_page_rule().get_secure() is True
	assert response.get_copy_page_rule().get_title() is False
	assert response.get_copy_page_rule().get_template() is True
	assert response.get_copy_page_rule().get_items() is True
	assert response.get_copy_page_rule().get_javascript_resource_assignments() is True
	assert response.get_copy_page_rule().get_cache_settings() is True
	assert response.get_copy_page_rule().get_settings() == merchantapi.model.CopyPageRule.PAGE_RULE_SETTINGS_ALL

