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


def test_availability_group_list_load_query():
	"""
	Tests the AvailabilityGroupList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupList_Load_Query.xml')

	availability_group_list_load_query_test_list_load()


def availability_group_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('name', 'AvailabilityGroupListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupListLoadQuery)

	assert isinstance(response.get_availability_groups(), list)

	for i, ag in enumerate(response.get_availability_groups()):
		assert isinstance(ag, merchantapi.model.AvailabilityGroup)
		assert ag.get_name() == ('AvailabilityGroupListLoadQueryTest_%d' % int(i+1))