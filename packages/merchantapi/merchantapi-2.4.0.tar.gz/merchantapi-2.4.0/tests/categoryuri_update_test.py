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


def test_category_uri_update():
	"""
	Tests the CategoryURI_Update API Call
	"""

	helper.provision_store('CategoryURI_Update.xml')

	category_uri_update_test_update()


def category_uri_update_test_update():
	category = helper.get_category('CategoryURIUpdateTest_1')

	assert category is not None
	assert len(category.get_uris()) == 2

	uri = None

	for u in category.get_uris():
		if u.get_canonical():
			continue
		uri = u
		break

	assert uri is not None

	test_uri = uri.get_uri() + '_1_1'

	request = merchantapi.request.CategoryURIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIUpdate)

	check = helper.get_category('CategoryURIUpdateTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None
