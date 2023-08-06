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


def test_availability_group_delete():
	"""
	Tests the AvailabilityGroup_Delete API Call
	"""

	helper.provision_store('AvailabilityGroup_Delete.xml')

	availability_group_delete_test_deletion()


def availability_group_delete_test_deletion():
	group = helper.get_availability_group('AvailabilityGroupDeleteTest_1')

	assert group is not None

	request = merchantapi.request.AvailabilityGroupDelete(helper.init_client(), group)

	assert request.get_availability_group_id() == group.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupDelete)

	check = helper.get_availability_group('AvailabilityGroupDeleteTest_1')

	assert check is None
