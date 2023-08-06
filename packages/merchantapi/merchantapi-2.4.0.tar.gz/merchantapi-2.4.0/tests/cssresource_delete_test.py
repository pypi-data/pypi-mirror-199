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


def test_cssresource_delete():
	"""
	Tests the CSSResource_Delete API Call
	"""

	helper.reset_branch_state()
	helper.provision_store('CSSResource_Delete.xml')

	cssresource_delete_test_deletion()


def cssresource_delete_test_deletion():
	request = merchantapi.request.CSSResourceDelete(helper.init_client())

	request.set_css_resource_code('CSSResource_Delete_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceDelete)

	check = helper.get_css_resource('CSSResource_Delete_1')

	assert check is None
