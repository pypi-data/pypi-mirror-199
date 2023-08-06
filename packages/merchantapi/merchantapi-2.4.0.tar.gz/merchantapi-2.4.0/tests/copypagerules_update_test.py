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


def test_copypagerules_update():
	"""
	Tests the CopyPageRules_Update API Call
	"""

	helper.provision_store('CopyPageRules_Update.xml')

	copypagerules_update_test_update()


def copypagerules_update_test_update():
	request = merchantapi.request.CopyPageRulesUpdate(helper.init_client())

	request.set_copy_page_rules_name('CopyPageRules_Update_1')
	request.set_name('CopyPageRules_Update_1_Updated')
	request.set_secure(True)
	request.set_title(True)
	request.set_template(True)
	request.set_items(True)
	request.set_javascript_resource_assignments(True)
	request.set_cache_settings(True)
	request.set_settings(merchantapi.model.CopyPageRule.PAGE_RULE_SETTINGS_NONE)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesUpdate)

	check = helper.get_copy_page_rule('CopyPageRules_Update_1_Updated')

	assert check is not None
	assert check.get_name() == 'CopyPageRules_Update_1_Updated'
	assert check.get_secure() is True
	assert check.get_title() is True
	assert check.get_template() is True
	assert check.get_items() is True
	assert check.get_javascript_resource_assignments() is True
	assert check.get_cache_settings() is True
	assert check.get_settings() == merchantapi.model.CopyPageRule.PAGE_RULE_SETTINGS_NONE
