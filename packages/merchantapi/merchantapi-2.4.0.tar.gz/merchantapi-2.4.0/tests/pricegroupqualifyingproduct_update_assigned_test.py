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


def test_price_group_qualifying_product_update_assigned():
	"""
	Tests the PriceGroupQualifyingProduct_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupQualifyingProduct_Update_Assigned.xml')

	price_group_qualifying_product_update_assigned_test_assignment()
	price_group_equalifying_product_update_assigned_test_unassignment()


def price_group_qualifying_product_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupQualifyingProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupQualifyingProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupQualifyingProductUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupQualifyingProductUpdateAssigned)

	check = helper.get_price_group_qualifying_products('PriceGroupQualifyingProductUpdateAssignedTest_1', 'PriceGroupQualifyingProductUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_equalifying_product_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupQualifyingProductUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupQualifyingProductUpdateAssignedTest_1')
	request.set_product_code('PriceGroupQualifyingProductUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupQualifyingProductUpdateAssigned)

	check = helper.get_price_group_excluded_products('PriceGroupQualifyingProductUpdateAssignedTest_1', 'PriceGroupQualifyingProductUpdateAssignedTest_2', False, True)

	assert len(check) == 1
