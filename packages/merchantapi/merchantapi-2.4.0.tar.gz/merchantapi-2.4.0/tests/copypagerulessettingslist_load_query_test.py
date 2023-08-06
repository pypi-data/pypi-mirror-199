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

valid_items = [ 'CopyPageRulesSettingsList_Load_Query_1', 'CopyPageRulesSettingsList_Load_Query_2', 'CopyPageRulesSettingsList_Load_Query_3', 'CopyPageRulesSettingsList_Load_Query_4' ]
valid_codes = [ 'templatefeed', 'discount_volume', 'cmp-cssui-vieworder', 'cmp-cssui-uslmltplattr' ]

def test_copypagerulessettingslist_load_query():
	"""
	Tests the CopyPageRulesSettingsList_Load_Query API Call
	"""

	helper.provision_store('CopyPageRulesSettingsList_Load_Query.xml')

	copypagerulessettingslist_load_query_test_load_all()
	copypagerulessettingslist_load_query_test_load_assigned()
	copypagerulessettingslist_load_query_test_load_unassigned()


def copypagerulessettingslist_load_query_test_load_all():
	request = merchantapi.request.CopyPageRulesSettingsListLoadQuery(helper.init_client())

	request.set_copy_page_rules_name('CopyPageRulesSettingsList_Load_Query_1')
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().like('code', 'CopyPageRulesSettingsList_Load_Query%')
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesSettingsListLoadQuery)

	assert len(response.get_copy_page_rules_settings()) == 4

	for s in response.get_copy_page_rules_settings():
		assert s.get_code() in valid_items
		assert s.get_module().get_code() in valid_codes


def copypagerulessettingslist_load_query_test_load_assigned():
	request = merchantapi.request.CopyPageRulesSettingsListLoadQuery(helper.init_client())

	request.set_copy_page_rules_name('CopyPageRulesSettingsList_Load_Query_1')
	request.set_assigned(True)
	request.set_unassigned(False)
	request.get_filters().like('code', 'CopyPageRulesSettingsList_Load_Query%')
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesSettingsListLoadQuery)

	assert len(response.get_copy_page_rules_settings()) == 2

	for s in response.get_copy_page_rules_settings():
		assert s.get_code() in valid_items
		assert s.get_module().get_code() in valid_codes


def copypagerulessettingslist_load_query_test_load_unassigned():
	request = merchantapi.request.CopyPageRulesSettingsListLoadQuery(helper.init_client())

	request.set_copy_page_rules_name('CopyPageRulesSettingsList_Load_Query_1')
	request.set_assigned(False)
	request.set_unassigned(True)
	request.get_filters().like('code', 'CopyPageRulesSettingsList_Load_Query%')
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesSettingsListLoadQuery)

	assert len(response.get_copy_page_rules_settings()) == 2

	for s in response.get_copy_page_rules_settings():
		assert s.get_code() in valid_items
		assert s.get_module().get_code() in valid_codes