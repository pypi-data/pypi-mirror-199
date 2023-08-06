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


def test_product_and_subscription_term_list_load_query():
	"""
	Tests the ProductAndSubscriptionTermList_Load_Query API Call
	"""

	helper.provision_store('ProductAndSubscriptionTermList_Load_Query.xml')

	product_and_subscription_term_list_load_query_test_list_load()


def product_and_subscription_term_list_load_query_test_list_load():
	codes = [ 'PASTLLQ_1', 'PASTLLQ_2' ]
	terms = [ 'daily', 'monthly' ]

	request = merchantapi.request.ProductAndSubscriptionTermListLoadQuery(helper.init_client())

	request.filters.is_in('code', ','.join(codes))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductAndSubscriptionTermListLoadQuery)

	assert len(response.get_product_and_subscription_terms()) is 3
	for term in response.get_product_and_subscription_terms():
		assert term.get_code() in codes
		assert term.get_term_frequency() in  terms
