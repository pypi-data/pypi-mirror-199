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


def test_attribute_template_attribute_update():
	"""
	Tests the AttributeTemplateAttribute_Update API Call
	"""

	helper.provision_store('AttributeTemplateAttribute_Update.xml')

	attribute_template_attribute_update_test_update()


def attribute_template_attribute_update_test_update():
	attribute = helper.get_attribute_template_attribute('ATAU_Template_1', 'ATAU_Attribute_1')

	assert attribute is not None

	request = merchantapi.request.AttributeTemplateAttributeUpdate(helper.init_client())

	request.set_attribute_template_code('ATAU_Template_1')
	request.set_attribute_template_attribute_code('ATAU_Attribute_1')
	request.set_code('ATAU_Attribute_1_Updated')
	request.set_prompt('ATAU_Attribute_1_Updated')
	request.set_price(1.12)
	request.set_cost(2.23)
	request.set_weight(3.34)
	request.set_type('checkbox')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeUpdate)

	check = helper.get_attribute_template_attribute('ATAU_Template_1', 'ATAU_Attribute_1_Updated')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_attribute_template_id() > 0
	assert check.get_code() == 'ATAU_Attribute_1_Updated'
	assert check.get_prompt() == 'ATAU_Attribute_1_Updated'
	assert check.get_type() == 'checkbox'
	assert check.get_price() == 1.12
	assert check.get_cost() == 2.23
	assert check.get_weight() == 3.34
