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


def test_availability_group_shipping_method_list_load_query():
	"""
	Tests the AvailabilityGroupShippingMethodList_Load_Query API Call
	"""

	helper.provision_store('AvailabilityGroupShippingMethodList_Load_Query.xml')

	availability_group_shipping_method_list_load_query_test_list_load()


def availability_group_shipping_method_list_load_query_test_list_load():
	request = merchantapi.request.AvailabilityGroupShippingMethodListLoadQuery(helper.init_client())

	request.set_availability_group_name('AvailGroupShpMthdListLoadQueryTest')
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AvailabilityGroupShippingMethodListLoadQuery)

	valid_codes = [
		'AvailGroupShpMthdListLoadQuery1',
		'AvailGroupShpMthdListLoadQuery2',
		'AvailGroupShpMthdListLoadQuery3',
		'AvailGroupShpMthdListLoadQuery4',
		'AvailGroupShpMthdListLoadQuery5',
	]

	assert len(response.get_availability_group_shipping_methods()) == 5

	for s in response.get_availability_group_shipping_methods():
		assert s.get_method_code() in valid_codes
