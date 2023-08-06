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


def test_coupon_customer_list_load_query():
	"""
	Tests the CouponCustomerList_Load_Query API Call
	"""

	helper.provision_store('CouponCustomerList_Load_Query.xml')

	coupon_customer_list_load_query_test_list_load()


def coupon_customer_list_load_query_test_list_load():
	coupon = helper.get_coupon('CouponCustomerListLoadQueryTest_1')

	assert coupon is not None

	request = merchantapi.request.CouponCustomerListLoadQuery(helper.init_client(), coupon)

	request.set_filters(request.filter_expression().like('login', 'CouponCustomerListLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponCustomerListLoadQuery)

	assert len(response.get_coupon_customers()) == 5
