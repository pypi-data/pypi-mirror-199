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


def test_category_product_update_assigned():
	"""
	Tests the CategoryProduct_Update_Assigned API Call
	"""

	helper.provision_store('CategoryProduct_Update_Assigned.xml')

	category_product_update_assigned_test_assignment()
	category_product_update_assigned_test_unassignment()
	category_product_update_assigned_test_invalid_assign()
	category_product_update_assigned_test_invalid_category()
	category_product_update_assigned_test_invalid_product()


def category_product_update_assigned_test_assignment():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_unassignment():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_invalid_assign():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_invalid_category():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('InvalidCategory')\
		.set_edit_product('CategoryProductUpdateAssignedTest_Product')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryProductUpdateAssigned)


def category_product_update_assigned_test_invalid_product():
	request = merchantapi.request.CategoryProductUpdateAssigned(helper.init_client())

	request.set_edit_category('CategoryProductUpdateAssignedTest_Category')\
		.set_edit_product('InvalidProduct')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryProductUpdateAssigned)
