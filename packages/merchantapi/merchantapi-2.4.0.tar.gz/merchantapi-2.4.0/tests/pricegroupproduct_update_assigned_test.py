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


def test_price_group_product_update_assigned():
	"""
	Tests the PriceGroupProduct_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupProduct_Update_Assigned.xml')

	price_group_product_update_assigned_test_assignment()
	price_group_product_update_assigned_test_unassignment()
	price_group_product_update_assigned_test_invalid_assign()
	price_group_product_update_assigned_test_invalid_price_group()
	price_group_product_update_assigned_test_invalid_product()


def price_group_product_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_invalid_assign():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	# noinspection PyTypeChecker
	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned('foobar')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_invalid_price_group():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('PriceGroupProductUpdateAssignedTest_1')\
		.set_price_group_name('InvalidPriceGroup')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupProductUpdateAssigned)


def price_group_product_update_assigned_test_invalid_product():
	request = merchantapi.request.PriceGroupProductUpdateAssigned(helper.init_client())

	request.set_product_code('InvalidProduct')\
		.set_price_group_name('PriceGroupProductUpdateAssignedTest')\
		.set_assigned(True)

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PriceGroupProductUpdateAssigned)
