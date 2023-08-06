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


def test_category_uri_insert():
	"""
	Tests the CategoryURI_Insert API Call
	"""

	helper.provision_store('CategoryURI_Insert.xml')

	category_uri_insert_test_insertion()


def category_uri_insert_test_insertion():
	test_uri = '/CategoryURIInsertTest_1_1'
	category = helper.get_category('CategoryURIInsertTest_1')

	assert category is not None

	request = merchantapi.request.CategoryURIInsert(helper.init_client(), category)

	request.set_uri(test_uri)
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_category('CategoryURIInsertTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None
