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


def test_product_variant_list_load_query():
	"""
	Tests the ProductVariantList_Load_Query API Call
	"""

	helper.provision_store('ProductVariantList_Load_Query.xml')

	product_variant_list_load_query_test_list_load()


def product_variant_list_load_query_test_list_load():
	product = helper.get_product('ProductVariantListLoadQueryTest_1')

	assert product is not None

	request = merchantapi.request.ProductVariantListLoadQuery(helper.init_client())

	request.set_product_code(product.get_code())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantListLoadQuery)

	assert len(response.get_product_variants()) > 0

	for v in response.get_product_variants():
		assert product.get_id() == v.get_product_id()
		assert len(v.get_attributes()) == 5

		for attribute in v.get_attributes():
			assert isinstance(attribute, merchantapi.model.ProductVariantAttribute)
			assert attribute.get_attribute_id() > 0
			assert len(attribute.get_attribute_code()) > 0
			assert attribute.get_option_id() is not None
			assert attribute.get_option_code() is not None