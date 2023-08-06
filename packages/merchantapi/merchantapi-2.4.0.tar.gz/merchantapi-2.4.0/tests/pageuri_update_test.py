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


def test_page_uri_update():
	"""
	Tests the PageURI_Update API Call
	"""

	helper.provision_store('PageURI_Update.xml')

	page_uri_update_test_update()


def page_uri_update_test_update():
	uris = helper.get_page_uris('PageURIUpdateTest_1')

	assert len(uris) == 2

	test_uri = '/PageURIUpdateTest_1_1_1'

	request = merchantapi.request.PageURIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIUpdate)

	check = helper.get_page_uris('PageURIUpdateTest_1')

	uri = None
	for u in check:
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None
