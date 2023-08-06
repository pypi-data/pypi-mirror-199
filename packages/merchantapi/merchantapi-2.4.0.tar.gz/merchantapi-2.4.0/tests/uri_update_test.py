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


def test_uri_update():
	"""
	Tests the URI_Update API Call
	"""

	helper.provision_store('URI_Update.xml')

	uri_update_test_update_product()
	uri_update_test_update_category()
	uri_update_test_update_feed()
	uri_update_test_update_page()


def uri_update_test_update_product():
	test_uri = '/uri-update-product-test-api'

	product = helper.get_product('UriUpdateTest')

	assert len(product.get_uris()) == 1

	uri = product.get_uris()[0]

	request = merchantapi.request.URIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(product.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PRODUCT)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = None
	for u in helper.get_product(product.get_code()).get_uris():
		if u.get_id() == uri.get_id():
			check_uri = u

	assert check_uri is not None


def uri_update_test_update_category():
	test_uri = '/uri-update-category-test-api'

	category = helper.get_category('UriUpdateTest')

	assert len(category.get_uris()) == 1

	uri = category.get_uris()[0]

	request = merchantapi.request.URIUpdate(helper.init_client(), uri)

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination(category.get_code())
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_CATEGORY)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = None
	for u in helper.get_category(category.get_code()).get_uris():
		if u.get_id() == uri.get_id():
			check_uri = u

	assert check_uri is not None



def uri_update_test_update_feed():
	test_uri = '/uri-update-feed-test-api'

	uris = helper.get_feed_uris('UriUpdateTest_1')

	assert len(uris) > 0

	request = merchantapi.request.URIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriUpdateTest_1')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_FEED)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = helper.get_uri(test_uri)

	assert check_uri is not None
	assert check_uri.get_id() == uris[0].get_id()



def uri_update_test_update_page():
	test_uri = '/uri-update-page-test-api'

	uris = helper.get_page_uris('UriUpdateTest_2')

	assert len(uris) > 0

	request = merchantapi.request.URIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)
	request.set_canonical(False)
	request.set_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination('UriUpdateTest_2')
	request.set_destination_type(merchantapi.model.Uri.DESTINATION_TYPE_PAGE)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIUpdate)

	check_uri = helper.get_uri(test_uri)

	assert check_uri is not None
	assert check_uri.get_id() == uris[0].get_id()
