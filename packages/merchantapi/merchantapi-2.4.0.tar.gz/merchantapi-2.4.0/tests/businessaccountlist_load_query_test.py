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


def test_business_account_list_load_query():
	"""
	Tests the BusinessAccountList_Load_Query API Call
	"""

	helper.provision_store('BusinessAccountList_Load_Query.xml')

	business_account_list_load_query_test_list_load()


def business_account_list_load_query_test_list_load():
	request = merchantapi.request.BusinessAccountListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('title', 'BusinessAccountListLoadQueryTest%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountListLoadQuery)

	assert len(response.get_business_accounts()) == 7
