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


def test_product_delete():
	"""
	Tests the Product_Delete API Call
	"""

	helper.provision_store('Product_Delete.xml')

	product_delete_test_deletion_by_id()
	product_delete_test_deletion_by_code()
	product_delete_test_deletion_by_sku()
	product_delete_test_deletion_by_edit_product()


def product_delete_test_deletion_by_id():
	product = helper.get_product('ProductDeleteTest_ID')

	assert isinstance(product, merchantapi.model.Product)

	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_product_id(product.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_ID')

	assert check is None


def product_delete_test_deletion_by_code():
	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_product_code('ProductDeleteTest_CODE')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_CODE')

	assert check is None


def product_delete_test_deletion_by_sku():
	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_product_sku('ProductDeleteTest_SKU')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_SKU')

	assert check is None


def product_delete_test_deletion_by_edit_product():
	request = merchantapi.request.ProductDelete(helper.init_client())

	request.set_edit_product('ProductDeleteTest_EDIT_PRODUCT')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductDelete)

	check = helper.get_product('ProductDeleteTest_EDIT_PRODUCT')

	assert check is None
