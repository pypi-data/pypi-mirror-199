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


def test_page_uri_insert():
	"""
	Tests the PageURI_Insert API Call
	"""

	helper.provision_store('PageURI_Insert.xml')

	page_uri_insert_test_insertion()


def page_uri_insert_test_insertion():
	test_uri = '/PageURIInsertTest_1_1'
	uris = helper.get_page_uris('PageURIInsertTest_1')

	assert len(uris) == 1

	request = merchantapi.request.PageURIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_page_code('PageURIInsertTest_1')
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIInsert)

	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_page_uris('PageURIInsertTest_1')
	uri = None

	for u in check:
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None
