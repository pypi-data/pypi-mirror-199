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


def test_availability_group_update():
	"""
	Tests the AvailabilityGroup_Update API Call
	"""

	helper.provision_store('AvailabilityGroup_Update.xml')

	availability_group_update_test_update()


def availability_group_update_test_update():
	group = helper.get_availability_group('AvailabilityGroupUpdateTest_1')

	assert group is not None

	request = merchantapi.request.AvailabilityGroupUpdate(helper.init_client(), group)

	request.set_availability_group_name('AvailabilityGroupUpdateTest_1_Modified')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupUpdate)

	checkA = helper.get_availability_group('AvailabilityGroupUpdateTest_1')
	checkB = helper.get_availability_group('AvailabilityGroupUpdateTest_1_Modified')

	assert checkA is None
	assert checkB is not None
