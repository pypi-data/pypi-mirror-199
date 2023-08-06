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


def test_product_variant_list_delete():
	"""
	Tests the ProductVariantList_Delete API Call
	"""

	helper.provision_store('ProductVariantList_Delete.xml')

	product_variant_list_delete_test_deletion()


def product_variant_list_delete_test_deletion():
	product = helper.get_product('ProductVariantListDeleteTest_1')

	assert product is not None

	variants = helper.get_product_variants(product.get_code())

	assert len(variants) > 0

	request = merchantapi.request.ProductVariantListDelete(helper.init_client())

	request.set_product_code(product.get_code())

	for v in variants:
		request.add_product_variant(v)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductVariantListDelete)

	check_variants = helper.get_product_variants(product.get_code())

	for v in variants:
		for cv in check_variants:
			assert cv.get_variant_id() != v.get_variant_id()
