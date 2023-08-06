"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
import time
from . import helper


def test_coupon_insert():
	"""
	Tests the Coupon_Insert API Call
	"""

	helper.provision_store('Coupon_Insert.xml')

	coupon_insert_test_insertion()
	coupon_insert_test_insertion_with_price_group()
	coupon_insert_test_duplicate_code()
	coupon_insert_test_invalid_price_group()


def coupon_insert_test_insertion():
	request = merchantapi.request.CouponInsert(helper.init_client())

	start_time = int(time.time() / 1000) - 1000
	end_time = int(time.time() / 1000) + 100000

	request.set_code('CouponInsertTest_1')\
		.set_description('CouponInsertTest_1 Description')\
		.set_customer_scope(merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS)\
		.set_date_time_start(start_time)\
		.set_date_time_end(end_time)\
		.set_max_per(1)\
		.set_max_use(2)\
		.set_active(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponInsert)
	assert isinstance(response.get_coupon(), merchantapi.model.Coupon)
	assert response.get_coupon().get_code() == 'CouponInsertTest_1'
	assert response.get_coupon().get_description() == 'CouponInsertTest_1 Description'
	assert response.get_coupon().get_customer_scope() == merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS
	assert response.get_coupon().get_date_time_start() == start_time
	assert response.get_coupon().get_date_time_end() == end_time
	assert response.get_coupon().get_max_per() == 1
	assert response.get_coupon().get_max_use() == 2
	assert response.get_coupon().get_active() is True

	coupon = helper.get_coupon('CouponInsertTest_1')

	assert isinstance(coupon, merchantapi.model.Coupon)
	assert coupon.get_id() == response.get_coupon().get_id()


def coupon_insert_test_insertion_with_price_group():
	price_group = helper.get_price_group('CouponInsertTest_PriceGroup')

	assert isinstance(price_group, merchantapi.model.PriceGroup)
	assert price_group.get_id() > 0

	request = merchantapi.request.CouponInsert(helper.init_client())

	start_time = int(time.time() / 1000) - 1000
	end_time = int(time.time() / 1000) + 100000

	request.set_code('CouponInsertTest_2')\
		.set_description('CouponInsertTest_2 Description')\
		.set_customer_scope(merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS)\
		.set_date_time_start(start_time)\
		.set_date_time_end(end_time)\
		.set_max_per(1)\
		.set_max_use(2)\
		.set_active(True)\
		.set_price_group_id(price_group.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponInsert)
	assert isinstance(response.get_coupon(), merchantapi.model.Coupon)
	assert response.get_coupon().get_code() == 'CouponInsertTest_2'
	assert response.get_coupon().get_description() == 'CouponInsertTest_2 Description'
	assert response.get_coupon().get_customer_scope() == merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS
	assert response.get_coupon().get_date_time_start() == start_time
	assert response.get_coupon().get_date_time_end() == end_time
	assert response.get_coupon().get_max_per() == 1
	assert response.get_coupon().get_max_use() == 2
	assert response.get_coupon().get_active() is True

	coupon = helper.get_coupon('CouponInsertTest_2')

	assert isinstance(coupon, merchantapi.model.Coupon)
	assert coupon.get_id() == response.get_coupon().get_id()


def coupon_insert_test_duplicate_code():
	request = merchantapi.request.CouponInsert(helper.init_client())

	request.set_code('CouponInsertTest_Duplicate')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponInsert)


def coupon_insert_test_invalid_price_group():
	request = merchantapi.request.CouponInsert(helper.init_client())

	start_time = int(time.time() / 1000) - 1000
	end_time = int(time.time() / 1000) + 100000

	request.set_code('CouponInsertTest_2')\
		.set_description('CouponInsertTest_2 Description')\
		.set_customer_scope(merchantapi.model.Coupon.CUSTOMER_SCOPE_ALL_SHOPPERS)\
		.set_date_time_start(start_time)\
		.set_date_time_end(end_time)\
		.set_max_per(1)\
		.set_max_use(2)\
		.set_active(True)\
		.set_price_group_id(8569545)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CouponInsert)
