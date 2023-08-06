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


def test_uri_list_load_query():
	"""
	Tests the URIList_Load_Query API Call
	"""

	helper.provision_store('URIList_Load_Query.xml')

	uri_list_load_query_test_list_load()


def uri_list_load_query_test_list_load():
	request = merchantapi.request.URIListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIListLoadQuery)

	assert len(response.get_uris()) > 0
