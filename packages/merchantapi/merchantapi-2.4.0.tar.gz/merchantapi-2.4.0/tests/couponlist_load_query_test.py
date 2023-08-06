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


def test_coupon_list_load_query():
	"""
	Tests the CouponList_Load_Query API Call
	"""

	helper.provision_store('CouponList_Load_Query.xml')

	coupon_list_load_query_test_list_load()


def coupon_list_load_query_test_list_load():
	request = merchantapi.request.CouponListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'CouponListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponListLoadQuery)

	assert isinstance(response.get_coupons(), list)
	assert len(response.get_coupons()) == 3

	for i, coupon in enumerate(response.get_coupons()):
		assert isinstance(coupon, merchantapi.model.Coupon)
		assert coupon.get_code() == 'CouponListLoadQueryTest_%d' % int(i+1)
