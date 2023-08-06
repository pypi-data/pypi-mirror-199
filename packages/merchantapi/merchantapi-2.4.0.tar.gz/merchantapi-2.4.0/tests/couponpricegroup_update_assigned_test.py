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


def test_coupon_price_group_update_assigned():
	"""
	Tests the CouponPriceGroup_Update_Assigned API Call
	"""

	helper.provision_store('CouponPriceGroup_Update_Assigned.xml')

	coupon_price_group_update_assigned_test_assignment()
	coupon_price_group_update_assigned_test_unassignment()
	coupon_price_group_update_assigned_test_invalid_assign()
	coupon_price_group_update_assigned_invalid_price_group()
	coupon_price_group_update_assigned_invalid_coupon()


def coupon_price_group_update_assigned_test_assignment():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_test_unassignment():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_test_invalid_assign():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_invalid_price_group():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('CouponPriceGroupUpdateAssignedTest_Coupon')\
		.set_price_group_name('InvalidPriceGroup')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponPriceGroupUpdateAssigned)


def coupon_price_group_update_assigned_invalid_coupon():
	request = merchantapi.request.CouponPriceGroupUpdateAssigned(helper.init_client())

	request.set_coupon_code('InvalidCoupon')\
		.set_price_group_name('CouponPriceGroupUpdateAssignedTest_PriceGroup_1')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponPriceGroupUpdateAssigned)
