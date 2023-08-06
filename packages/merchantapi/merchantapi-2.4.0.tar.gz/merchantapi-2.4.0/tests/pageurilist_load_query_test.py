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


def test_page_uri_list_load_query():
	"""
	Tests the PageURIList_Load_Query API Call
	"""

	helper.provision_store('PageURIList_Load_Query.xml')

	page_uri_list_load_query_test_list_load()


def page_uri_list_load_query_test_list_load():
	request = merchantapi.request.PageURIListLoadQuery(helper.init_client())

	request.set_page_code('PageURIListLoadQueryTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageURIListLoadQuery)

	assert len(response.get_uris()) == 7
