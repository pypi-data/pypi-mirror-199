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


def test_child_category_list_load_query():
	"""
	Tests the ChildCategoryList_Load_Query API Call
	"""

	helper.provision_store('ChildCategoryList_Load_Query.xml')

	child_category_list_load_query_test_list_load_assigned()
	child_category_list_load_query_test_list_load_assigned_code()
	child_category_list_load_query_test_list_load_unassigned()


def child_category_list_load_query_test_list_load_assigned():
	category = helper.get_category('ChildCategoryListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.ChildCategoryListLoadQuery(helper.init_client(), category)

	request.set_assigned(True)
	request.set_unassigned(False)

	assert request.get_parent_category_id() > 0

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChildCategoryListLoadQuery)

	assert len(response.get_categories()) == 6


def child_category_list_load_query_test_list_load_assigned_code():
	category = helper.get_category('ChildCategoryListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.ChildCategoryListLoadQuery(helper.init_client())

	request.set_parent_category_code('ChildCategoryListLoadQueryTest_1')
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChildCategoryListLoadQuery)

	assert len(response.get_categories()) == 6


def child_category_list_load_query_test_list_load_unassigned():
	category = helper.get_category('ChildCategoryListLoadQueryTest_1')

	assert category is not None

	request = merchantapi.request.ChildCategoryListLoadQuery(helper.init_client(), category)

	request.set_filters(request.filter_expression().like('code', 'ChildCategoryListLoadQueryTest%'))
	request.set_assigned(False)
	request.set_unassigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChildCategoryListLoadQuery)

	assert len(response.get_categories()) == 2
