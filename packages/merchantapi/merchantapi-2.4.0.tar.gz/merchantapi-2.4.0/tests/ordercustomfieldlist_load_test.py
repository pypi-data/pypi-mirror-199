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


def test_order_custom_field_list_load():
	"""
	Tests the OrderCustomFieldList_Load API Call
	"""

	helper.provision_store('OrderCustomFieldList_Load.xml')

	order_custom_field_list_load_test_list_load()


def order_custom_field_list_load_test_list_load():
	request = merchantapi.request.OrderCustomFieldListLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCustomFieldListLoad)

	assert isinstance(response.get_order_custom_fields(), list)
	assert len(response.get_order_custom_fields()) > 1

	for ocf in response.get_order_custom_fields():
		assert isinstance(ocf, merchantapi.model.OrderCustomField)
