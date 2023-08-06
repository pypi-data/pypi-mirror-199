"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from . import helper
import merchantapi.multicall
import merchantapi.request
import merchantapi.response
import time
import random

helper.configure_logging()


def test_multiple_request_types():
	request = merchantapi.multicall.MultiCallRequest(helper.init_client())

	request.add_request(merchantapi.request.ProductListLoadQuery())
	request.add_request(merchantapi.request.CategoryListLoadQuery())
	request.add_request(merchantapi.request.CouponListLoadQuery())
	request.add_request(merchantapi.request.PriceGroupListLoadQuery())

	response = request.send()

	helper.validate_response_success(response, merchantapi.multicall.MultiCallResponse)

	helper.validate_response_success(response.get_responses()[0], merchantapi.response.ProductListLoadQuery)
	helper.validate_response_success(response.get_responses()[1], merchantapi.response.CategoryListLoadQuery)
	helper.validate_response_success(response.get_responses()[2], merchantapi.response.CouponListLoadQuery)
	helper.validate_response_success(response.get_responses()[3], merchantapi.response.PriceGroupListLoadQuery)


def test_using_operations():
	request = merchantapi.multicall.MultiCallRequest(helper.init_client())
	operation = request.operation()

	ctime = int(time.time())

	for i in range(1, 5):
		insert = merchantapi.request.ProductInsert(None)

		insert.set_product_code('foo_%d' % int(ctime + random.random())) \
			.set_product_sku('foo_%d' % int(ctime + random.random())) \
			.set_product_name('foo_%d' % int(ctime + random.random()))

		operation.add_request(insert)

	cat_insert = merchantapi.request.CategoryInsert(None)

	cat_insert.set_category_code('foo_%d' % ctime) \
		.set_category_name('foo_%d' % ctime)

	request.add_request(cat_insert)

	response = request.send()

	helper.validate_response_success(response, merchantapi.multicall.MultiCallResponse)


def test_failure():
	client = helper.init_client()

	client.get_authenticator().set_api_token('InvalidToken')

	request = merchantapi.multicall.MultiCallRequest(client)

	request.add_request(merchantapi.request.ProductListLoadQuery())

	response = request.send()

	helper.validate_response_error(response, merchantapi.multicall.MultiCallResponse)


def test_timeout():
	helper.provision_store('MulticallTimeout.xml')

	timeout_test_timeout()
	timeout_test_timeout_with_continue()


def timeout_test_timeout():
	client = helper.init_client()
	client.set_option('operation_timeout', 1)

	request = merchantapi.multicall.MultiCallRequest(client)
	request.set_auto_timeout_continue(False)

	for i in range(1, 500):
		addreq = merchantapi.request.ProductListLoadQuery()
		addreq.set_filters(addreq.filter_expression().equal('code', 'MultiTimeoutTest%d' % i))

		request.add_request(addreq)

	response = request.send()

	assert response.is_timeout() is True


def timeout_test_timeout_with_continue():
	client = helper.init_client()
	client.set_option('operation_timeout', 1)

	request = merchantapi.multicall.MultiCallRequest(client)
	request.set_auto_timeout_continue(True)

	for i in range(1, 500):
		addreq = merchantapi.request.ProductListLoadQuery()
		addreq.set_filters(addreq.filter_expression().equal('code', 'MultiTimeoutTest%d' % i))

		request.add_request(addreq)

	response = request.send()

	helper.validate_response_success(response, merchantapi.multicall.MultiCallResponse)

	assert response.is_timeout() is False
	assert len(request.get_requests()) == len(response.data)

	for i, resp in enumerate(response.get_responses(), 0):
		helper.validate_response_success(resp, merchantapi.response.ProductListLoadQuery)
		assert len(resp.get_products()) == 1
		assert resp.get_products()[0].get_code() == 'MultiTimeoutTest%d' % (i+1)
