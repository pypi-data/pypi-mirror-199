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


def test_uri_list_delete():
	"""
	Tests the URIList_Delete API Call
	"""

	helper.provision_store('URIList_Delete.xml')

	uri_list_delete_test_deletion()


def uri_list_delete_test_deletion():
	product = helper.get_product('URIListDeleteTest_1')

	assert product is not None
	assert len(product.get_uris()) > 1

	request = merchantapi.request.URIListDelete(helper.init_client())
	
	for u in product.get_uris():
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.URIListDelete)

	assert len(helper.get_product(product.get_code()).get_uris()) == 1
