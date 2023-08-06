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


def test_customer_history_list_load_query():
	"""
	Tests the CustomerCreditHistoryList_Load_Query API Call
	"""

	helper.provision_store('CustomerCreditHistoryList_Load_Query.xml')

	customer_history_list_load_query_test_list_load()


def customer_history_list_load_query_test_list_load():
	customer = helper.get_customer('CustomerHistoryListLoadQuery')

	assert customer is not None

	for i in range(0, 3):
		insert_request = merchantapi.request.CustomerCreditHistoryInsert(helper.init_client(), customer)
		insert_request.set_amount(1.99)
		insert_request.set_description('DESCRIPTION')
		insert_request.set_transaction_reference('REFERENCE')
		helper.validate_response_success(insert_request.send(), merchantapi.response.CustomerCreditHistoryInsert)

	request = merchantapi.request.CustomerCreditHistoryListLoadQuery(helper.init_client(), customer)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerCreditHistoryListLoadQuery)

	assert len(response.get_customer_credit_history()) == 3
	for history in response.get_customer_credit_history():
		assert isinstance(history, merchantapi.model.CustomerCreditHistory)
		assert history.get_description() == 'DESCRIPTION'
		assert history.get_transaction_reference() == 'REFERENCE'
		assert history.get_amount() == 1.99
