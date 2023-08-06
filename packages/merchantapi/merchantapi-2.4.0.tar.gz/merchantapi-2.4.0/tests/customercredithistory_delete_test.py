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


def test_customer_history_delete():
	"""
	Tests the CustomerCreditHistory_Delete API Call
	"""

	helper.provision_store('CustomerCreditHistory_Delete.xml')

	customer_history_delete_test_deletion()


def customer_history_delete_test_deletion():
	customer = helper.get_customer('CustomerCreditHistoryDelete')

	assert customer is not None

	add_request = merchantapi.request.CustomerCreditHistoryInsert(helper.init_client(), customer)

	assert add_request.get_customer_id() == customer.get_id()

	add_request.set_amount(1.99)
	add_request.set_description('DESCRIPTION')
	add_request.set_transaction_reference('REFERENCE')

	add_response = add_request.send()

	helper.validate_response_success(add_response, merchantapi.response.CustomerCreditHistoryInsert)

	load_request = merchantapi.request.CustomerCreditHistoryListLoadQuery(helper.init_client(), customer)

	load_response = load_request.send()

	helper.validate_response_success(load_response, merchantapi.response.CustomerCreditHistoryListLoadQuery)

	assert len(load_response.get_customer_credit_history()) == 1

	history = load_response.get_customer_credit_history()[0]

	assert isinstance(history, merchantapi.model.CustomerCreditHistory)

	request = merchantapi.request.CustomerCreditHistoryDelete(helper.init_client(), history)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerCreditHistoryDelete)
