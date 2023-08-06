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


def test_product_insert():
	"""
	Tests the Product_Insert API Call
	"""

	helper.provision_store('Product_Insert.xml')
	helper.upload_image('graphics/ProductInsert.jpg')

	product_insert_test_insertion()
	product_insert_test_insertion_with_custom_fields()
	product_insert_test_duplicate()


def product_insert_test_insertion():
	request = merchantapi.request.ProductInsert(helper.init_client())

	request.set_product_code('ProductInsertTest_1') \
		.set_product_sku('ProductInsertTest_1_Sku') \
		.set_product_name('API Inserted Product 1') \
		.set_product_active(True) \
		.set_product_price(7.50) \
		.set_product_cost(7.50)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductInsert)

	product = helper.get_product('ProductInsertTest_1')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_code() == 'ProductInsertTest_1'
	assert product.get_sku() == 'ProductInsertTest_1_Sku'
	assert product.get_name() == 'API Inserted Product 1'
	assert product.get_price() == 7.50
	assert product.get_cost() == 7.50
	assert product.get_id() > 0


def product_insert_test_insertion_with_custom_fields():
	request = merchantapi.request.ProductInsert(helper.init_client())

	request.set_product_code('ProductInsertTest_2') \
		.set_product_sku('ProductInsertTest_2_Sku') \
		.set_product_name('API Inserted Product 2') \
		.set_product_active(True) \
		.set_product_price(7.50) \
		.set_product_cost(7.50)

	request.get_custom_field_values() \
		.add_value('ProductInsertTest_checkbox', 'True', 'customfields') \
		.add_value('ProductInsertTest_imageupload', 'graphics/00000001/ProductInsert.jpg', 'customfields') \
		.add_value('ProductInsertTest_text', 'ProductInsertTest_2', 'customfields') \
		.add_value('ProductInsertTest_textarea', 'ProductInsertTest_2', 'customfields') \
		.add_value('ProductInsertTest_dropdown', 'Option2', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductInsert)

	product = helper.get_product('ProductInsertTest_2')

	assert isinstance(product, merchantapi.model.Product)
	assert product.get_code() == 'ProductInsertTest_2'
	assert product.get_sku() == 'ProductInsertTest_2_Sku'
	assert product.get_name() == 'API Inserted Product 2'
	assert product.get_price() == 7.50
	assert product.get_cost() == 7.50
	assert product.get_id() > 0
	assert product.get_custom_field_values().has_value('ProductInsertTest_checkbox', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_checkbox', 'customfields') == '1'
	assert product.get_custom_field_values().has_value('ProductInsertTest_imageupload', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_imageupload', 'customfields') == 'graphics/00000001/ProductInsert.jpg'
	assert product.get_custom_field_values().has_value('ProductInsertTest_text', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_text', 'customfields') == 'ProductInsertTest_2'
	assert product.get_custom_field_values().has_value('ProductInsertTest_textarea', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_textarea', 'customfields') == 'ProductInsertTest_2'
	assert product.get_custom_field_values().has_value('ProductInsertTest_dropdown', 'customfields') is True
	assert product.get_custom_field_values().get_value('ProductInsertTest_dropdown', 'customfields') == 'Option2'


def product_insert_test_duplicate():
	request = merchantapi.request.ProductInsert(helper.init_client())

	request.set_product_code('ProductInsertTest_Duplicate') \
		.set_product_sku('ProductInsertTest_Duplicate_Sku') \
		.set_product_name('API Inserted Product Duplicate') \
		.set_product_active(True) \
		.set_product_price(7.50) \
		.set_product_cost(7.50)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.ProductInsert)
