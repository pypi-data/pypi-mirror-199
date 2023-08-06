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


def test_uri_delete():
	"""
	Tests the URI_Delete API Call
	"""

	helper.provision_store('URI_Delete.xml')

	uri_delete_test_deletion()



def uri_delete_test_deletion():
	product = helper.get_product('URIDeleteTest_1')

	assert product is not None
	assert len(product.get_uris()) > 1

	uri = None

	for u in product.get_uris():
		if u.get_canonical():
			uri = u
			break

	assert uri is not None

	request = merchantapi.request.URIDelete(helper.init_client(), uri)
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIDelete)

	check_uri = None
	for u in helper.get_product(product.get_code()).get_uris():
		if u.get_id() == uri.get_id():
			check_uri = u
			break

	assert check_uri is None
