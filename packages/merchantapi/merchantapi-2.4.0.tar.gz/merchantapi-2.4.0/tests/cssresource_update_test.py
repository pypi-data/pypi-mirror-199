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


def test_cssresource_update():
	"""
	Tests the CSSResource_Update API Call
	"""

	helper.reset_branch_state()
	helper.provision_store('CSSResource_Update.xml')

	cssresource_update_test_update()


def cssresource_update_test_update():
	request = merchantapi.request.CSSResourceUpdate(helper.init_client())

	request.set_css_resource_code('CSSResource_Update_1')
	request.set_css_resource_file_path('/mm5/some/other/resource.css')
	request.set_css_resource_global(False)
	request.set_css_resource_active(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceUpdate)

	check = helper.get_css_resource('CSSResource_Update_1')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'CSSResource_Update_1'
	assert check.get_file() == '/mm5/some/other/resource.css'
	assert check.get_is_global() == False
	assert check.get_active() == False
