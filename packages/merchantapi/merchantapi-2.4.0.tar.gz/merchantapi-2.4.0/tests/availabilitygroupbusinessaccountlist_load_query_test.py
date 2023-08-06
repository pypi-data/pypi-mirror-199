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


def test_availability_group_business_account_list_load_query():
	"""
	Tests the AvailabilityGroupBusinessAccountList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupBusinessAccountList_Load_Query.xml')

	availability_group_business_account_list_load_query_test_list_load()


def availability_group_business_account_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupBusinessAccountListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGBALLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('title', 'AGBALLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupBusinessAccountListLoadQuery)

	valid_titles = [
		'AGBALLoadQueryTest_1',
		'AGBALLoadQueryTest_2',
		'AGBALLoadQueryTest_3',
		'AGBALLoadQueryTest_4',
		'AGBALLoadQueryTest_5',
	]

	assert len(response.get_availability_group_business_accounts()) == 5

	for b in response.get_availability_group_business_accounts():
		assert b.get_title() in valid_titles
