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


def test_javascriptresourcelist_load_query():
	"""
	Tests the JavaScriptResourceList_Load_Query API Call
	"""

	helper.provision_store('JavaScriptResourceList_Load_Query.xml')

	javascriptresourcelist_load_query_test_listload()


def javascriptresourcelist_load_query_test_listload():
	request = merchantapi.request.JavaScriptResourceListLoadQuery(helper.init_client())

	request.get_filters().like('code', 'JavaScriptResourceListLoadQueryTest%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceListLoadQuery)

	assert len(response.get_javascript_resources()) == 5

	for resource in response.get_javascript_resources():
		assert resource.get_code().startswith('JavaScriptResourceListLoadQueryTest')
