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
from . credentials import MerchantApiTestCredentials


def test_category_uri_redirect():
	"""
	Tests the CategoryURI_Redirect API Call
	"""

	helper.provision_store('CategoryURI_Redirect.xml')

	category_uri_redirect_test_redirect()


def category_uri_redirect_test_redirect():
	category_a = helper.get_category('CategoryURIRedirectTest_1')
	category_b = helper.get_category('CategoryURIRedirectTest_2')

	assert category_a is not None
	assert category_b is not None
	assert len(category_a.get_uris()) == 3
	assert len(category_b.get_uris()) == 3

	request = merchantapi.request.CategoryURIRedirect(helper.init_client())

	request.set_destination(category_a.get_code())
	request.set_destination_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination_type('category')
	request.set_status(301)

	for u in category_b.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIRedirect)

	category_b_check = helper.get_category('CategoryURIRedirectTest_2')

	assert category_b_check is not None
	assert len(category_b_check.get_uris()) == 1
