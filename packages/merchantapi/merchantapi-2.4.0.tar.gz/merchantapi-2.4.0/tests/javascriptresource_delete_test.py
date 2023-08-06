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


def test_javascriptresource_delete():
	"""
	Tests the JavaScriptResource_Delete API Call
	"""

	helper.reset_branch_state()
	helper.provision_store('JavaScriptResource_Delete.xml')

	javascriptresource_delete_test_deletion()


def javascriptresource_delete_test_deletion():
	request = merchantapi.request.JavaScriptResourceDelete(helper.init_client())

	request.set_javascript_resource_code('JavaScriptResource_Delete_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceDelete)

	check = helper.get_javascript_resource('JavaScriptResource_Delete_1')

	assert check is None
