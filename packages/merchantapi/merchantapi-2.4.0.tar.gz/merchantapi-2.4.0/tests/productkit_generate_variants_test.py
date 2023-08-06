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


def test_product_kit_generate_variants():
	"""
	Tests the ProductKit_Generate_Variants API Call
	"""

	helper.provision_store('ProductKit_Generate_Variants.xml')

	product_kit_generate_variants_test_generation()


def product_kit_generate_variants_test_generation():
	product = helper.get_product('ProductKitGenerateVariantsTest_1')

	assert product is not None

	request = merchantapi.request.ProductKitGenerateVariants(helper.init_client(), product)

	request.set_pricing_method(request.VARIANT_PRICING_METHOD_MASTER)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductKitGenerateVariants)

	assert helper.get_product_kit_variant_count(product.get_code()) == 4
