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


def test_copypageruleslist_load_query():
	"""
	Tests the CopyPageRulesList_Load_Query API Call
	"""

	helper.provision_store('CopyPageRulesList_Load_Query.xml')

	copypageruleslist_load_query_test_load()


def copypageruleslist_load_query_test_load():
	request = merchantapi.request.CopyPageRulesListLoadQuery(helper.init_client())

	request.get_filters().like('name', 'CopyPageRulesList_Load_Query%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyPageRulesListLoadQuery)

	assert len(response.get_copy_page_rules()) == 3
