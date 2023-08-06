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


def test_price_group_customer_list_load_query():
	"""
	Tests the PriceGroupCustomerList_Load_Query API Call
	"""

	helper.provision_store('PriceGroupCustomerList_Load_Query.xml')

	price_group_customer_list_load_query_test_list_load()


def price_group_customer_list_load_query_test_list_load():
	request = merchantapi.request.PriceGroupCustomerListLoadQuery(helper.init_client())

	request.set_price_group_name('PriceGroupCustomerListLoadQueryTest') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupCustomerListLoadQuery)

	assert isinstance(response.get_price_group_customers(), list)
	assert len(response.get_price_group_customers()) == 5

	for i, pgc in enumerate(response.get_price_group_customers()):
		assert isinstance(pgc, merchantapi.model.PriceGroupCustomer)
		assert pgc.get_login() == 'PriceGroupCustomerListLoadQueryTest_0%d' % int(i+1)
		assert pgc.get_business_title() == 'PriceGroupCustomerListLoadQueryTest'
		assert pgc.get_assigned() is True
