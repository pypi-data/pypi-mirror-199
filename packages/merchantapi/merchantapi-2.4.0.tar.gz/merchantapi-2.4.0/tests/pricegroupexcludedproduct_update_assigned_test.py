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


def test_price_group_excluded_product_update_assigned():
	"""
	Tests the PriceGroupExcludedProduct_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupExcludedProduct_Update_Assigned.xml')

	price_group_excluded_product_update_assigned_test_assignment()
	price_group_excluded_product_update_assigned_test_unassignment()


def price_group_excluded_product_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupExcludedProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupExcludedProductUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedProductUpdateAssigned)

	check = helper.get_price_group_excluded_products('PriceGroupExcludedProductUpdateAssignedTest_1', 'PriceGroupExcludedProductUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_excluded_product_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupExcludedProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupExcludedProductUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedProductUpdateAssigned)

	check = helper.get_price_group_excluded_products('PriceGroupExcludedProductUpdateAssignedTest_1', 'PriceGroupExcludedProductUpdateAssignedTest_2', False, True)

	assert len(check) == 1
