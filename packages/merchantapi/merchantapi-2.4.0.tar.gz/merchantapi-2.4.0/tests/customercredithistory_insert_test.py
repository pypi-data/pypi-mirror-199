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


def test_customer_history_insert():
	"""
	Tests the CustomerCreditHistory_Insert API Call
	"""

	helper.provision_store('CustomerCreditHistory_Insert.xml')

	customer_history_insert_test_insertion()


def customer_history_insert_test_insertion():
	customer = helper.get_customer('CustomerCreditHistoryInsert')

	assert customer is not None

	request = merchantapi.request.CustomerCreditHistoryInsert(helper.init_client(), customer)

	assert request.get_customer_id() == customer.get_id()

	request.set_amount(1.99)
	request.set_description('DESCRIPTION')
	request.set_transaction_reference('REFERENCE')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerCreditHistoryInsert)
