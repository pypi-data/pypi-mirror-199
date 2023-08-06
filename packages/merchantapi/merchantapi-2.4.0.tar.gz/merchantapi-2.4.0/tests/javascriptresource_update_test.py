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


def test_javascriptresource_update():
	"""
	Tests the JavaScriptResource_Update API Call
	"""

	helper.reset_branch_state()
	helper.provision_store('JavaScriptResource_Update.xml')

	javascriptresource_update_test_update()


def javascriptresource_update_test_update():
	request = merchantapi.request.JavaScriptResourceUpdate(helper.init_client())

	request.set_javascript_resource_code('JavaScriptResource_Update_1')
	request.set_javascript_resource_file_path('/mm5/some/other/resource.js')
	request.set_javascript_resource_global(False)
	request.set_javascript_resource_active(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceUpdate)

	check = helper.get_javascript_resource('JavaScriptResource_Update_1')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'JavaScriptResource_Update_1'
	assert check.get_file() == '/mm5/some/other/resource.js'
	assert check.get_is_global() == False
	assert check.get_active() == False
