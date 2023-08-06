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


def test_order_custom_fields_update():
	"""
	Tests the OrderCustomFields_Update API Call
	"""

	helper.provision_store('OrderCustomFields_Update.xml')

	order_custom_fields_update_test_update()


def order_custom_fields_update_test_update():
	request = merchantapi.request.OrderCustomFieldsUpdate(helper.init_client())

	request.set_order_id(65191651)

	request.get_custom_field_values()\
		.add_value('OrderCustomFieldsUpdate_Field_1', 'foobar')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCustomFieldsUpdate)

	order = helper.get_order(65191651)

	assert isinstance(order, merchantapi.model.Order)
	assert isinstance(order.get_custom_field_values(), merchantapi.model.CustomFieldValues)
	assert order.get_custom_field_values().get_value('OrderCustomFieldsUpdate_Field_1') == 'foobar'
