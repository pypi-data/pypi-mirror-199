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


def test_product_image_update_type():
	"""
	Tests the ProductImage_Update_Type API Call
	"""

	helper.provision_store('ProductImage_Update_Type_Clear.xml')
	helper.upload_image('graphics/ProductImageUpdateTypeTest.jpg')
	helper.provision_store('ProductImage_Update_Type.xml')

	product_image_update_type_test_update()


def product_image_update_type_test_update():
	product = helper.get_product('ProductImageUpdateTypeTest')

	assert product is not None
	assert len(product.get_product_image_data()) == 1

	image_types_request = merchantapi.request.ImageTypeListLoadQuery(helper.init_client())
	image_types_request.set_filters(image_types_request.filter_expression().equal('code', 'ProductImageUpdateTypeTestB'))

	image_types_response = image_types_request.send()

	assert len(image_types_response.get_image_types()) == 1

	request = merchantapi.request.ProductImageUpdateType(helper.init_client())

	request.set_product_image_id(product.get_product_image_data()[0].get_id())
	request.set_image_type_id(image_types_response.get_image_types()[0].get_id())

	response = request.send()

	check = helper.get_product('ProductImageUpdateTypeTest')

	assert check is not None
	assert len(check.get_product_image_data()) == 1
	assert check.get_product_image_data()[0].get_type_id() == image_types_response.get_image_types()[0].get_id()
