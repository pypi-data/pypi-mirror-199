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


def test_copypagerulessettings_update_assigned():
	"""
	Tests the CopyPageRulesSettings_Update_Assigned API Call
	"""

	helper.provision_store('CopyPageRulesSettings_Update_Assigned.xml')

	copypagerulessettings_update_assigned_test_assignment()
	copypagerulessettings_update_assigned_test_unassignment()


def copypagerulessettings_update_assigned_test_assignment():
	request = merchantapi.request.CopyPageRulesSettingsUpdateAssigned(helper.init_client())

	request.set_copy_page_rules_name('CopyPageRulesSettings_Update_Assigned_1')
	request.set_item_code('CopyPageRulesSettings_Update_Assigned_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesSettingsUpdateAssigned)
	
	check = get_copy_page_rules_settings_item('CopyPageRulesSettings_Update_Assigned_1', 'CopyPageRulesSettings_Update_Assigned_1')
	assert check is not None
	assert check.get_assigned() is True

def copypagerulessettings_update_assigned_test_unassignment():
	request = merchantapi.request.CopyPageRulesSettingsUpdateAssigned(helper.init_client())

	request.set_copy_page_rules_name('CopyPageRulesSettings_Update_Assigned_1')
	request.set_item_code('CopyPageRulesSettings_Update_Assigned_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesSettingsUpdateAssigned)

	check = get_copy_page_rules_settings_item('CopyPageRulesSettings_Update_Assigned_1', 'CopyPageRulesSettings_Update_Assigned_2')
	assert check is not None
	assert check.get_assigned() is False


def get_copy_page_rules_settings_item(name: str, item_code: str):
	request = merchantapi.request.CopyPageRulesSettingsListLoadQuery(helper.init_client())

	request.set_copy_page_rules_name(name)
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().equal('code', item_code)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesSettingsListLoadQuery)

	return response.get_copy_page_rules_settings()[0] if len(response.get_copy_page_rules_settings()) else None