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


def test_product_uri_insert():
	"""
	Tests the ProductURI_Insert API Call
	"""

	helper.provision_store('ProductURI_Insert.xml')

	product_uri_insert_test_insertion()


def product_uri_insert_test_insertion():
	test_uri = '/ProductURIInsertTest_1_1'
	product = helper.get_product('ProductURIInsertTest_1')

	assert product is not None

	request = merchantapi.request.ProductURIInsert(helper.init_client(), product)

	request.set_uri(test_uri)
	request.set_canonical(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductURIInsert)
	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_product('ProductURIInsertTest_1')
	uri = None

	assert check is not None

	for u in check.get_uris():
		if u.get_uri() == test_uri:
			uri = u
			break

	assert uri is not None
