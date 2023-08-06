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


def test_coupon_update():
	"""
	Tests the Coupon_Update API Call
	"""

	helper.provision_store('Coupon_Update.xml')

	coupon_update_test_update()


def coupon_update_test_update():
	request = merchantapi.request.CouponUpdate(helper.init_client())

	request.set_edit_coupon('CouponUpdateTest')\
		.set_max_use(1000)\
		.set_max_per(2)\
		.set_active(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponUpdate)

	coupon = helper.get_coupon('CouponUpdateTest')

	assert isinstance(coupon, merchantapi.model.Coupon)
	assert coupon.get_code() == 'CouponUpdateTest'
	assert coupon.get_max_per() == 2
	assert coupon.get_max_use() == 1000
	assert coupon.get_active() is True
