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


def test_coupon_customer_update_assigned():
	"""
	Tests the CouponCustomer_Update_Assigned API Call
	"""

	helper.provision_store('CouponCustomer_Update_Assigned.xml')

	coupon_customer_update_assigned_test_assignment()
	coupon_customer_update_assigned_test_unassignment()


def coupon_customer_update_assigned_test_assignment():
	coupon = helper.get_coupon('CouponCustomerUpdateAssignedTest_1')

	assert coupon is not None

	request = merchantapi.request.CouponCustomerUpdateAssigned(helper.init_client(), coupon)

	request.set_customer_login('CouponCustomerUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponCustomerUpdateAssigned)

	check = helper.get_coupon_customers('CouponCustomerUpdateAssignedTest_1', 'CouponCustomerUpdateAssignedTest_1', True, False)

	assert check is not None
	assert len(check) == 1


def coupon_customer_update_assigned_test_unassignment():
	coupon = helper.get_coupon('CouponCustomerUpdateAssignedTest_1')

	assert coupon is not None

	request = merchantapi.request.CouponCustomerUpdateAssigned(helper.init_client(), coupon)

	request.set_customer_login('CouponCustomerUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponCustomerUpdateAssigned)

	check = helper.get_coupon_customers('CouponCustomerUpdateAssignedTest_1', 'CouponCustomerUpdateAssignedTest_2', False, True)

	assert check is not None
	assert len(check) == 1
