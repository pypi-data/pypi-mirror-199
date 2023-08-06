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


def test_store_list_load_query():
	"""
	Tests the StoreList_Load_Query API Call
	"""

	store_list_load_query_test_load()


def store_list_load_query_test_load():
	request = merchantapi.request.StoreListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreListLoadQuery)

	assert len(response.get_stores()) >= 1
	for store in response.get_stores():
		assert isinstance(store, merchantapi.model.Store)
