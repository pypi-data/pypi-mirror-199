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


def test_product_image_delete():
	"""
	Tests the ProductImage_Delete API Call
	"""

	helper.provision_store('ProductImage_Delete_Cleanup_v10.xml')
	helper.upload_image('graphics/ProductImageDelete.jpg')
	helper.provision_store('ProductImage_Delete_v10.xml')

	product_image_delete_test_deletion()


def product_image_delete_test_deletion():
	product = helper.get_product('ProductImageDeleteTest')

	assert isinstance(product, merchantapi.model.Product)
	assert isinstance(product.get_product_image_data(), list)
	assert len(product.get_product_image_data()) == 1

	request = merchantapi.request.ProductImageDelete(helper.init_client(), product.get_product_image_data()[0])

	assert request.get_product_image_id() == product.get_product_image_data()[0].get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductImageDelete)
