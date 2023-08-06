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


def test_product_variant_generate():
	"""
	Tests the ProductVariant_Generate API Call
	"""

	helper.provision_store('ProductVariant_Generate.xml')

	product_variant_generate_test_generation()


def product_variant_generate_test_generation():
	product = helper.get_product('ProductVariantGenerateTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) == 0

	request = merchantapi.request.ProductVariantGenerate(helper.init_client())
	request.set_product_code(product.get_code())
	request.set_pricing_method(request.VARIANT_PRICING_METHOD_MASTER);

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantGenerate)

	check_variants = helper.get_product_variants(product.get_code())

	assert len(check_variants) > 0
