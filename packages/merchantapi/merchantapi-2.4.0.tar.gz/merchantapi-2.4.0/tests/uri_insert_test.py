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
from . credentials import MerchantApiTestCredentials


def test_uri_insert():
	"""
	Tests the URI_Insert API Call
	"""

	helper.provision_store('URI_Insert.xml')

	uri_insert_test_insertion_product()
	uri_insert_test_insertion_category()
	uri_insert_test_insertion_feed()
	uri_insert_test_insertion_page()


def uri_insert_test_insertion_product():
	test_uri = '/uri-insert-product-test-api'

	product = helper.get_product('UriInsertTest')

	for uri in product.get_uris():
		assert uri.get_uri() != test_uri

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(product.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PRODUCT)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri


def uri_insert_test_insertion_category():
	test_uri = '/uri-insert-category-test-api'

	category = helper.get_category('UriInsertTest')

	for uri in category.get_uris():
		assert uri.get_uri() != test_uri

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(category.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_CATEGORY)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri


def uri_insert_test_insertion_feed():
	test_uri = '/uri-insert-feed-test-api'

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriInsertTest_1')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_FEED)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_uri(test_uri)

	assert check is not None
	assert check.get_feed_id() > 0


def uri_insert_test_insertion_page():
	test_uri = '/uri-insert-page-test-api'

	request = merchantapi.request.URIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriInsertTest_2')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PAGE)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIInsert)

	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_uri(test_uri)

	assert check is not None
	assert check.get_page_id() > 0
