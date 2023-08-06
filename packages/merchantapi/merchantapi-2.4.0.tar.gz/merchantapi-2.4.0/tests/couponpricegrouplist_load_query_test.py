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


def test_coupon_price_group_list_load_query():
	"""
	Tests the CouponPriceGroupList_Load_Query API Call
	"""

	helper.provision_store('CouponPriceGroupList_Load_Query.xml')

	coupon_price_group_list_load_query_test_list_load()


def coupon_price_group_list_load_query_test_list_load():
	request = merchantapi.request.CouponPriceGroupListLoadQuery(helper.init_client())

	request.set_coupon_code('CouponPriceGroupListLoadQueryTest_Coupon') \
		.set_assigned(True) \
		.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponPriceGroupListLoadQuery)

	assert isinstance(response.get_coupon_price_groups(), list)
	assert len(response.get_coupon_price_groups()) == 3

	for i, cp in enumerate(response.get_coupon_price_groups()):
		assert isinstance(cp, merchantapi.model.CouponPriceGroup)
		assert cp.get_name() == 'CouponPriceGroupListLoadQueryTest_PriceGroup_%d' % int(i+1)
