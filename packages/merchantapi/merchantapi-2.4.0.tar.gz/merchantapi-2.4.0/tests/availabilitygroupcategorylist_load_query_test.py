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


def test_availability_group_category_list_load_query():
	"""
	Tests the AvailabilityGroupCategoryList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupCategoryList_Load_Query.xml')

	availability_group_category_list_load_query_test_list_load()


def availability_group_category_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupCategoryListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGCATLLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'AGCATLLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupCategoryListLoadQuery)

	valid_codes = [
		'AGCATLLoadQueryTest_1',
		'AGCATLLoadQueryTest_2',
		'AGCATLLoadQueryTest_3',
		'AGCATLLoadQueryTest_4',
		'AGCATLLoadQueryTest_5'
	]

	assert len(response.get_availability_group_categories()) == 5

	for c in response.get_availability_group_categories():
		assert c.get_code() in valid_codes
