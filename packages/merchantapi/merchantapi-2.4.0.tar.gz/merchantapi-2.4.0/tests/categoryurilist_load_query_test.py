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


def test_category_uri_list_load_query():
	"""
	Tests the CategoryURIList_Load_Query API Call
	"""

	helper.provision_store('CategoryURIList_Load_Query.xml')

	category_uri_list_load_query_test_list_load()


def category_uri_list_load_query_test_list_load():
	category = helper.get_category('CategoryURIListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.CategoryURIListLoadQuery(helper.init_client(), category)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryURIListLoadQuery)

	assert len(response.get_uris()) > 1

	for uri in response.get_uris():
		assert uri.get_category_id() == category.get_id()
		if uri.get_canonical():
			continue
		assert 'CategoryURIListLoadQueryTest' in uri.get_uri()
