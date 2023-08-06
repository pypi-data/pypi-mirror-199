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


def test_product_variant_insert():
	"""
	Tests the ProductVariant_Insert API Call
	"""

	helper.provision_store('ProductVariant_Insert.xml')

	product_variant_insert_test_insertion()
	product_variant_insert_test_insertion_by_codes()


def product_variant_insert_test_insertion():
	product = helper.get_product('ProductVariantInsertTest_1')
	part_a = helper.get_product('ProductVariantInsertTest_1_1')
	part_b = helper.get_product('ProductVariantInsertTest_1_2')

	assert product is not None
	assert part_a is not None
	assert part_b is not None

	request = merchantapi.request.ProductVariantInsert(helper.init_client(), product)

	attr = merchantapi.model.VariantAttribute()

	attr.set_attribute_id(product.get_attributes()[0].get_id())
	attr.set_attribute_template_attribute_id(0)
	attr.set_option_id(product.get_attributes()[0].get_options()[0].get_id())

	request.add_variant_attribute(attr)

	part_1 = merchantapi.model.VariantPart()
	part_2 = merchantapi.model.VariantPart()

	part_1.set_part_id(part_a.get_id())
	part_1.set_quantity(1)

	part_2.set_part_id(part_b.get_id())
	part_2.set_quantity(1)

	request.add_variant_part(part_1)
	request.add_variant_part(part_2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantInsert)

	assert response.get_product_variant().get_product_id() == product.get_id()
	assert response.get_product_variant().get_variant_id() > 0

	assert len(response.get_product_variant().get_attributes()) == 1
	assert response.get_product_variant().get_attributes()[0].get_attribute_id() == product.get_attributes()[0].get_id()
	assert response.get_product_variant().get_attributes()[0].get_option_id() == product.get_attributes()[0].get_options()[0].get_id()


def product_variant_insert_test_insertion_by_codes():
	product = helper.get_product('ProductVariantInsertTest_1')
	part_a = helper.get_product('ProductVariantInsertTest_1_1')
	part_b = helper.get_product('ProductVariantInsertTest_1_2')

	assert product is not None
	assert part_a is not None
	assert part_b is not None

	request = merchantapi.request.ProductVariantInsert(helper.init_client(), product)

	attr = merchantapi.model.VariantAttribute()

	attr.set_attribute_code(product.get_attributes()[0].get_code())
	attr.set_option_code(product.get_attributes()[0].get_options()[0].get_code())

	request.add_variant_attribute(attr)

	part_1 = merchantapi.model.VariantPart()
	part_2 = merchantapi.model.VariantPart()

	part_1.set_part_code(part_a.get_code())
	part_1.set_quantity(1)

	part_2.set_part_code(part_b.get_code())
	part_2.set_quantity(1)

	request.add_variant_part(part_1)
	request.add_variant_part(part_2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantInsert)

	assert response.get_product_variant().get_product_id() == product.get_id()
	assert response.get_product_variant().get_variant_id() > 0

	assert len(response.get_product_variant().get_attributes()) == 1
	assert response.get_product_variant().get_attributes()[0].get_attribute_id() == product.get_attributes()[0].get_id()
	assert response.get_product_variant().get_attributes()[0].get_option_id() == product.get_attributes()[0].get_options()[0].get_id()