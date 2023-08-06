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


def test_product_kit_variant_count():
	"""
	Tests the ProductKit_Variant_Count API Call
	"""

	helper.provision_store('ProductKit_Variant_Count.xml')

	product_kit_variant_count_test_count()


def product_kit_variant_count_test_count():
	product = helper.get_product('ProductKitVariantCountTest_1')

	request = merchantapi.request.ProductKitVariantCount(helper.init_client(), product)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductKitVariantCount)

	assert response.get_variants() == 4
