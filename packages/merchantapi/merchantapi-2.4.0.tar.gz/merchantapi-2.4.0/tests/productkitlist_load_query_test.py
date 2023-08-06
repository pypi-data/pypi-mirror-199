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


def test_product_kit_list_load_query():
	"""
	Tests the ProductKitList_Load_Query API Call
	"""

	helper.provision_store('ProductKitList_Load_Query.xml')

	product_kit_list_load_query_test_list_load()


def product_kit_list_load_query_test_list_load():
	product = helper.get_product('ProductKitListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.ProductKitListLoadQuery(helper.init_client(), product)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductKitListLoadQuery)

	assert len(response.get_product_kits()) > 0
