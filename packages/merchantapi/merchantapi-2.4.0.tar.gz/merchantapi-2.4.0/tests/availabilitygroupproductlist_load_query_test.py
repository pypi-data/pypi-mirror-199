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


def test_availability_group_product_list_load_query():
	"""
	Tests the AvailabilityGroupProductList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupProductList_Load_Query.xml')

	availability_group_product_list_load_query_test_list_load()


def availability_group_product_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupProductListLoadQuery(helper.init_client())

	request.set_availability_group_name('AGPRODLLoadQueryTest_1')
	request.set_filters(request.filter_expression().like('code', 'AGPRODLLoadQueryTest%'))
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupProductListLoadQuery)

	assert len(response.get_availability_group_products()) == 5

	valid_codes = [
		'AGPRODLLoadQueryTest_1',
		'AGPRODLLoadQueryTest_2',
		'AGPRODLLoadQueryTest_3',
		'AGPRODLLoadQueryTest_4',
		'AGPRODLLoadQueryTest_5'
	]

	for p in response.get_availability_group_products():
		assert p.get_code() in valid_codes
