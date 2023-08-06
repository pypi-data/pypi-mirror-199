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


def test_product_image_add():
	"""
	Tests the ProductImage_Add API Call
	"""

	helper.upload_image('graphics/ProductImageAdd.jpg')
	helper.provision_store('ProductImage_Add.xml')

	product_image_add_test_add()
	product_image_add_test_invalid_product()
	product_image_add_test_invalid_product_path()


def product_image_add_test_add():
	request = merchantapi.request.ProductImageAdd(helper.init_client())

	request.set_product_code('ProductImageAddTest') \
		.set_filepath('graphics/00000001/1/ProductImageAdd.jpg') \
		.set_image_type_id(0)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductImageAdd)
	assert isinstance(response.get_product_image_data(), merchantapi.model.ProductImageData)
	assert response.get_product_image_data().get_id() > 0


def product_image_add_test_invalid_product():
	request = merchantapi.request.ProductImageAdd(helper.init_client())

	request.set_product_code('InvalidProductImageAddTest') \
		.set_filepath('graphics/00000001/1/ProductImageAdd.jpg') \
		.set_image_type_id(0)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.ProductImageAdd)


def product_image_add_test_invalid_product_path():
	request = merchantapi.request.ProductImageAdd(helper.init_client())

	request.set_product_code('ProductImageAddTest') \
		.set_filepath('graphics/00000001/InvalidImage.jpg') \
		.set_image_type_id(0)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.ProductImageAdd)
