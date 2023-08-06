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


def test_price_group_excluded_category_update_assigned():
	"""
	Tests the PriceGroupExcludedCategory_Update_Assigned API Call
	"""

	helper.provision_store('PriceGroupExcludedCategory_Update_Assigned.xml')

	price_group_excluded_category_update_assigned_test_assignment()
	price_group_excluded_category_update_assigned_test_unassignment()


def price_group_excluded_category_update_assigned_test_assignment():
	request = merchantapi.request.PriceGroupExcludedCategoryUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedCategoryUpdateAssignedTest_1')
	request.set_category_code('PriceGroupExcludedCategoryUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryUpdateAssigned)

	check = helper.get_price_group_excluded_categories('PriceGroupExcludedCategoryUpdateAssignedTest_1', 'PriceGroupExcludedCategoryUpdateAssignedTest_1', True, False)

	assert len(check) == 1


def price_group_excluded_category_update_assigned_test_unassignment():
	request = merchantapi.request.PriceGroupExcludedCategoryUpdateAssigned(helper.init_client())

	request.set_price_group_name('PriceGroupExcludedCategoryUpdateAssignedTest_1')
	request.set_category_code('PriceGroupExcludedCategoryUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PriceGroupExcludedCategoryUpdateAssigned)

	check = helper.get_price_group_excluded_categories('PriceGroupExcludedCategoryUpdateAssignedTest_1', 'PriceGroupExcludedCategoryUpdateAssignedTest_2', False, True)

	assert len(check) == 1
