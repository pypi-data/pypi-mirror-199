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


def test_product_copy():
	"""
	Tests the Product_Copy API Call
	"""

	helper.provision_store('Product_Copy.xml')

	product_copy_test_copy()
	product_copy_test_copy_with_rules()
	product_copy_test_copy_with_recycle()


def product_copy_test_copy():
	check = helper.get_product('ProductCopyTest_1_Copy')
	assert check == None

	request = merchantapi.request.ProductCopy(helper.init_client())

	request.set_source_product_code('ProductCopyTest_1')
	request.set_destination_product_code('ProductCopyTest_1_Copy')
	request.set_destination_product_name('ProductCopyTest_1_Copy')

	response = request.send()

	assert response.get_product() is not None
	assert response.get_completed() is True

	helper.validate_response_success(response, merchantapi.response.ProductCopy)

	check = helper.get_product('ProductCopyTest_1_Copy')

	assert check is not None


def product_copy_test_copy_with_rules():
	check = helper.get_product('ProductCopyTest_2_Copy')
	assert check == None

	request = merchantapi.request.ProductCopy(helper.init_client())

	request.set_source_product_code('ProductCopyTest_2')
	request.set_destination_product_code('ProductCopyTest_2_Copy')
	request.set_destination_product_name('ProductCopyTest_2_Copy')
	request.set_copy_product_rules_name('ProductCopyTest_Rules_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductCopy)
	
	assert response.get_product() is not None
	assert response.get_completed() is True

	check = helper.get_product('ProductCopyTest_2_Copy')

	assert check is not None


def product_copy_test_copy_with_recycle():
	check = helper.get_product('ProductCopyRecycleTest_Copy')
	assert check == None

	request = merchantapi.request.ProductCopy(helper.init_client())

	request.set_source_product_code('ProductCopyRecycleTest')
	request.set_destination_product_code('ProductCopyRecycleTest_Copy')
	request.set_destination_product_name('ProductCopyRecycleTest_Copy')
	request.set_copy_product_rules_name('ProductCopyRecycleTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductCopy)
	
	assert response.get_product() is None
	assert response.get_completed() is False
	assert response.get_product_copy_session_id() is not None

	request.set_product_copy_session_id(response.get_product_copy_session_id())

	final_response = request.send()

	helper.validate_response_success(final_response, merchantapi.response.ProductCopy)
	
	assert final_response.get_product() is not None
	assert final_response.get_completed() is True