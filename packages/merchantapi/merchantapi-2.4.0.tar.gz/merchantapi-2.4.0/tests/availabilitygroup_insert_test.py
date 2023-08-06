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


def test_availability_group_insert():
	"""
	Tests the AvailabilityGroup_Insert API Call
	"""

	helper.provision_store('AvailabilityGroup_Insert.xml')

	availability_group_insert_test_insertion()


def availability_group_insert_test_insertion():
	group = helper.get_availability_group('AvailabilityGroupInsertTest_1')

	assert group is None

	request = merchantapi.request.AvailabilityGroupInsert(helper.init_client())

	request.set_availability_group_name('AvailabilityGroupInsertTest_1')
	request.set_availability_group_tax_exempt(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupInsert)

	assert isinstance(response.get_availability_group(), merchantapi.model.AvailabilityGroup)
	assert response.get_availability_group().get_name() == 'AvailabilityGroupInsertTest_1'
	assert response.get_availability_group().get_tax_exempt() is True

	check = helper.get_availability_group('AvailabilityGroupInsertTest_1')
	assert check is not None
	assert check.get_id() == response.get_availability_group().get_id()
