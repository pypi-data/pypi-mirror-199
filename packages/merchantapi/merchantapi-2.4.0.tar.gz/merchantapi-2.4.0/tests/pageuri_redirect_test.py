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


def test_page_uri_redirect():
	"""
	Tests the PageURI_Redirect API Call
	"""

	helper.provision_store('PageURI_Redirect.xml')

	page_uri_redirect_test_redirect()


def page_uri_redirect_test_redirect():
	page_a_uris = helper.get_page_uris('PageURIRedirectTest_1')
	page_b_uris = helper.get_page_uris('PageURIRedirectTest_2')

	assert len(page_a_uris) == 3
	assert len(page_b_uris) == 3

	request = merchantapi.request.PageURIRedirect(helper.init_client())

	request.set_destination('PageURIRedirectTest_1')
	request.set_destination_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination_type('page')
	request.set_status(301)

	for u in page_b_uris:
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIRedirect)

	page_b_check = helper.get_page_uris('PageURIRedirectTest_2')

	assert page_b_check is not None
	assert len(page_b_check) == 1
