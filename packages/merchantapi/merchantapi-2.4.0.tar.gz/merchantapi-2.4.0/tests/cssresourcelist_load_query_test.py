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


def test_cssresourcelist_load_query():
	"""
	Tests the CSSResourceList_Load_Query API Call
	"""

	helper.provision_store('CSSResourceList_Load_Query.xml')

	cssresourcelist_load_query_test_listload()


def cssresourcelist_load_query_test_listload():
	request = merchantapi.request.CSSResourceListLoadQuery(helper.init_client())

	request.get_filters().like('code', 'CSSResourceListLoadQueryTest%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceListLoadQuery)

	assert len(response.get_css_resources()) == 5

	for resource in response.get_css_resources():
		assert resource.get_code().startswith('CSSResourceListLoadQueryTest')
