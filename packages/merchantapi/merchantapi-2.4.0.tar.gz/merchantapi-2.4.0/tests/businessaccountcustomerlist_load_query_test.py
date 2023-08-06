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


def test_business_account_customer_list_load_query():
	"""
	Tests the BusinessAccountCustomerList_Load_Query API Call
	"""

	helper.provision_store('BusinessAccountCustomerList_Load_Query.xml')

	business_account_customer_list_load_query_test_list_load_assigned()
	business_account_customer_list_load_query_test_list_load_unassigned()


def business_account_customer_list_load_query_test_list_load_assigned():
	request = merchantapi.request.BusinessAccountCustomerListLoadQuery(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('login', 'BusinessAccountCustomerListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerListLoadQuery)

	assert len(response.get_business_account_customers()) == 5


def business_account_customer_list_load_query_test_list_load_unassigned():
	request = merchantapi.request.BusinessAccountCustomerListLoadQuery(helper.init_client())

	request.set_business_account_title('BusinessAccountCustomerListLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('login', 'BusinessAccountCustomerListLoadQueryTest%'))
	request.set_assigned(False)
	request.set_unassigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BusinessAccountCustomerListLoadQuery)

	assert len(response.get_business_account_customers()) == 1
