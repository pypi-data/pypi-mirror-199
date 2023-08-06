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


def test_category_uri_list_delete():
	"""
	Tests the CategoryURIList_Delete API Call
	"""

	helper.provision_store('CategoryURIList_Delete.xml')

	category_uri_list_delete_test_deletion()


def category_uri_list_delete_test_deletion():
	category = helper.get_category('CategoryURIListDeleteTest_1')

	assert category is not None
	assert len(category.get_uris()) > 1

	request = merchantapi.request.CategoryURIListDelete(helper.init_client())

	for u in category.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIListDelete)

	check = helper.get_category('CategoryURIListDeleteTest_1')

	assert check is not None
	assert len(check.get_uris()) == 1
