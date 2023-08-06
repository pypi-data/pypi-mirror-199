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


def test_availability_group_customer_list_load_query():
	"""
	Tests the AvailabilityGroupCustomerList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupCustomerList_Load_Query.xml')

	availability_group_customer_list_load_query_test_list_load()


def availability_group_customer_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupCustomerListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGCUSLLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('login', 'AGCUSLLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCustomerListLoadQuery)

	assert len(response.get_availability_group_customers()) == 5

	valid_logins = [
		'AGCUSLLoadQueryTest_1',
		'AGCUSLLoadQueryTest_2',
		'AGCUSLLoadQueryTest_3',
		'AGCUSLLoadQueryTest_4',
		'AGCUSLLoadQueryTest_5'
	]

	for c in response.get_availability_group_customers():
		assert c.get_login() in valid_logins
