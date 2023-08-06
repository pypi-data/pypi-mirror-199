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


def test_order_coupon_update_assigned():
	"""
	Tests the OrderPriceGroup_Update_Assigned API Call
	"""

	helper.provision_store('OrderCoupon_Update_Assigned.xml')

	order_coupon_update_assigned_test_assignment()
	order_coupon_update_assigned_test_unassignment()


def order_coupon_update_assigned_test_assignment():
	order = helper.get_order(3651500)

	assert order is not None

	request = merchantapi.request.OrderCouponUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_coupon_code('OrderCouponUpdateAssigned_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCouponUpdateAssigned)

	check_request = merchantapi.request.OrderCouponListLoadQuery(helper.init_client(), order)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(True)
	check_request.set_unassigned(False)
	check_request.set_filters(
		check_request.filter_expression()
		.equal('code', 'OrderCouponUpdateAssigned_1')
	)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderCouponListLoadQuery)

	assert len(check_response.get_order_coupons()) == 1
	assert check_response.get_order_coupons()[0].get_code() == 'OrderCouponUpdateAssigned_1'


def order_coupon_update_assigned_test_unassignment():
	order = helper.get_order(3651500)

	assert order is not None

	request = merchantapi.request.OrderCouponUpdateAssigned(helper.init_client(), order)

	assert order.get_id() == request.get_order_id()

	request.set_coupon_code('OrderCouponUpdateAssigned_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCouponUpdateAssigned)

	check_request = merchantapi.request.OrderCouponListLoadQuery(helper.init_client(), order)

	check_request.set_filters(
		check_request.filter_expression()
		.equal('code', 'OrderCouponUpdateAssigned_2')
	)

	assert order.get_id() == check_request.get_order_id()

	check_request.set_assigned(False)
	check_request.set_unassigned(True)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.OrderCouponListLoadQuery)

	assert len(check_response.get_order_coupons()) == 1
	assert check_response.get_order_coupons()[0].get_code() == 'OrderCouponUpdateAssigned_2'
