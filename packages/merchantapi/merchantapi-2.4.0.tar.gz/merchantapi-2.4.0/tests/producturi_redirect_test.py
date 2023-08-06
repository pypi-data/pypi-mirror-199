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


def test_product_uri_redirect():
	"""
	Tests the ProductURI_Redirect API Call
	"""

	helper.provision_store('ProductURI_Redirect.xml')

	product_uri_redirect_test_redirect()


def product_uri_redirect_test_redirect():
	product_a = helper.get_product('ProductURIRedirectTest_1')
	product_b = helper.get_product('ProductURIRedirectTest_2')

	assert product_a is not None
	assert product_b is not None
	assert len(product_a.get_uris()) == 3
	assert len(product_b.get_uris()) == 3

	request = merchantapi.request.ProductURIRedirect(helper.init_client())

	request.set_destination(product_a.get_code())
	request.set_destination_store_code(MerchantApiTestCredentials.MERCHANT_API_STORE_CODE)
	request.set_destination_type('product')
	request.set_status(301)

	for u in product_b.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIRedirect)

	product_b_check = helper.get_product('ProductURIRedirectTest_2')

	assert product_b_check is not None
	assert len(product_b_check.get_uris()) == 1
