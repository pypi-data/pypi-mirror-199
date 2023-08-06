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


def test_product_subscription_term_list_load_query():
	"""
	Tests the ProductSubscriptionTermList_Load_Query API Call
	"""

	helper.provision_store('ProductSubscriptionTermList_Load_Query.xml')

	product_subscription_term_list_load_query_test_list_load()


def product_subscription_term_list_load_query_test_list_load():
	terms = [ 'daily', 'weekly', 'monthly' ]
	descriptions = [ 'Daily', 'Weekly', 'Monthly' ]

	request = merchantapi.request.ProductSubscriptionTermListLoadQuery(helper.init_client())

	request.set_product_code('PSTLLQ_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductSubscriptionTermListLoadQuery)

	assert len(response.get_product_subscription_terms()) is 3
	for term in response.get_product_subscription_terms():
		assert term.get_frequency() in terms
		assert term.get_description() in  descriptions
