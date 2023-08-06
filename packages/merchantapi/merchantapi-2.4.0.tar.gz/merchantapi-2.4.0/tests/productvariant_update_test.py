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


def test_product_variant_update():
	"""
	Tests the ProductVariant_Update API Call
	"""

	helper.provision_store('ProductVariant_Update.xml')

	product_variant_update_test_update()


def product_variant_update_test_update():
	product = helper.get_product('ProductVariantUpdateTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) > 0

	for variant in variants:
		assert len(variant.get_parts()) > 0

		request = merchantapi.request.ProductVariantUpdate(helper.init_client())

		request.set_product_code(product.get_code())
		request.set_variant_id(variant.get_variant_id())

		for part in variant.get_parts():
			assert part.get_quantity() == 2

			variant_part = merchantapi.model.VariantPart()

			variant_part.set_part_id(part.get_product_id())
			variant_part.set_quantity(3)

			request.add_variant_part(variant_part)

		for dimension in variant.get_dimensions():
			variant_attr = merchantapi.model.VariantAttribute()
			variant_attr.set_attribute_id(dimension.get_attribute_id())
			variant_attr.set_attribute_template_attribute_id(dimension.get_attribute_template_attribute_id())
			variant_attr.set_option_id(dimension.get_option_id())

			request.add_variant_attribute(variant_attr)

		response = request.send()

		helper.validate_response_success(response, merchantapi.response.ProductVariantUpdate)

	for v in helper.get_product_variants(product.get_code()):
		for p in v.get_parts():
			assert p.get_quantity() ==3
