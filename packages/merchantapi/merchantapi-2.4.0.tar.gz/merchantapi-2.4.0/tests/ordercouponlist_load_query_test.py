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


def test_order_coupon_list_load_query():
	"""
	Tests the OrderCouponList_Load_Query API Call
	"""

	helper.provision_store('OrderCouponList_Load_Query.xml')

	order_coupon_list_load_query_test_list_load()


def order_coupon_list_load_query_test_list_load():
	order = helper.get_order(3651501)

	assert order is not None

	request = merchantapi.request.OrderCouponListLoadQuery(helper.init_client(), order)

	request.set_assigned(True)
	request.set_unassigned(False)

	assert order.get_id() == request.get_order_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCouponListLoadQuery)

	assert len(response.get_order_coupons()) == 3
	for order_coupon in response.get_order_coupons():
		assert isinstance(order_coupon, merchantapi.model.OrderCoupon)
		assert order_coupon.get_code() in ('OrderCouponList_Load_Query_1', 'OrderCouponList_Load_Query_2', 'OrderCouponList_Load_Query_3')
