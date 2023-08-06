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


def test_product_variant_list_load_product():
	"""
	Tests the ProductVariantList_Load_Product API Call
	"""

	helper.provision_store('ProductVariantList_Load_Product.xml')

	product_variant_list_load_product_test_load()


def product_variant_list_load_product_test_load():
	request = merchantapi.request.ProductVariantListLoadProduct(helper.init_client())

	request.set_edit_product('ProductVariantListLoadProduct') \
		.set_include_default_variant(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantListLoadProduct)

	assert isinstance(response.get_product_variants(), list)
	assert len(response.get_product_variants()) == 48

	for pv in response.get_product_variants():
		assert isinstance(pv, merchantapi.model.ProductVariant)
		assert isinstance(pv.get_parts(), list)
		assert len(pv.get_parts()) == 2

		for part in pv.get_parts():
			assert isinstance(part, merchantapi.model.ProductVariantPart)
			assert part.get_product_id() > 0
			assert 'PVLLP_' in part.get_product_code()

		assert isinstance(pv.get_dimensions(), list)
		assert len(pv.get_dimensions()) > 3

		for dimension in pv.get_dimensions():
			assert isinstance(dimension, merchantapi.model.ProductVariantDimension)
			assert dimension.get_attribute_id() > 0
