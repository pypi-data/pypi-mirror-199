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


def test_coupon_list_delete():
	"""
	Tests the CouponList_Delete API Call
	"""

	helper.provision_store('CouponList_Delete.xml')

	coupon_list_delete_test_deletion()


def coupon_list_delete_test_deletion():
	listrequest = merchantapi.request.CouponListLoadQuery(helper.init_client())

	listrequest.set_filters(listrequest.filter_expression().like('code', 'CouponListDeleteTest_%'))

	listresponse = listrequest.send()

	helper.validate_response_success(listresponse, merchantapi.response.CouponListLoadQuery)

	assert len(listresponse.get_coupons()) == 3

	request = merchantapi.request.CouponListDelete(helper.init_client())

	for coupon in listresponse.get_coupons():
		request.add_coupon(coupon)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponListDelete)
