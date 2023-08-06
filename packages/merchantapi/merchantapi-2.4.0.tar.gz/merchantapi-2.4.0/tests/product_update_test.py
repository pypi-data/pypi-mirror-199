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


def test_product_update():
	"""
	Tests the Product_Update API Call
	"""

	helper.provision_store('Product_Update.xml')

	product_update_test_update()
	product_update_test_update_code()


def product_update_test_update():
	request = merchantapi.request.ProductUpdate(helper.init_client())

	request.set_edit_product('ProductUpdateTest_1') \
		.set_product_name('ProductUpdateTest_1 New Name') \
		.set_product_price(39.99) \
		.set_product_cost(29.99) \
		.set_product_active(True) \
		.set_product_taxable(True) \
		.set_product_sku('ProductUpdateTest_1_Changed_SKU') \
		.set_product_page_title('ProductUpdateTest_1 Changed Page Title')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductUpdate)

	product = helper.get_product('ProductUpdateTest_1')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_name() == 'ProductUpdateTest_1 New Name'
	assert product.get_price() == 39.99
	assert product.get_cost() == 29.99
	assert product.get_active() is True
	assert product.get_taxable() is True
	assert product.get_sku() == 'ProductUpdateTest_1_Changed_SKU'
	assert product.get_page_title() == 'ProductUpdateTest_1 Changed Page Title'


def product_update_test_update_code():
	request = merchantapi.request.ProductUpdate(helper.init_client())

	request.set_edit_product('ProductUpdateTest_3') \
		.set_product_code('ProductUpdateTest_3_Changed')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductUpdate)

	product = helper.get_product('ProductUpdateTest_3_Changed')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_code() == 'ProductUpdateTest_3_Changed'
