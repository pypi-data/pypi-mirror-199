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


def test_customer_price_group_list_load_query():
	"""
	Tests the CustomerPriceGroupList_Load_Query API Call
	"""

	helper.provision_store('CustomerPriceGroupList_Load_Query.xml')

	customer_price_group_list_load_query_test_list_load()


def customer_price_group_list_load_query_test_list_load():
	request = merchantapi.request.CustomerPriceGroupListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerPriceGroupListLoadQueryTest') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerPriceGroupListLoadQuery)

	assert isinstance(response.get_customer_price_groups(), list)
	assert len(response.get_customer_price_groups()) == 3

	for i, customerpricegroup in enumerate(response.get_customer_price_groups()):
		assert isinstance(customerpricegroup, merchantapi.model.CustomerPriceGroup)
		assert customerpricegroup.get_name() == 'CustomerPriceGroupListLoadQueryTest_%d' % int(i+1)
		assert customerpricegroup.get_description() == 'CustomerPriceGroupListLoadQueryTest_%d' % int(i+1)
		assert customerpricegroup.get_customer_scope() == merchantapi.model.CustomerPriceGroup.ELIGIBILITY_CUSTOMER
		assert customerpricegroup.get_module().get_code() == 'discount_product'
