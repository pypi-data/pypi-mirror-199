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


def test_attribute_template_option_update():
	"""
	Tests the AttributeTemplateOption_Update API Call
	"""

	helper.provision_store('AttributeTemplateOption_Update.xml')

	attribute_template_option_update_test_update()


def attribute_template_option_update_test_update():
	request = merchantapi.request.AttributeTemplateOptionUpdate(helper.init_client())

	request.set_attribute_template_code('ATOU_Template_1')
	request.set_attribute_template_attribute_code('ATOU_Attribute_1')
	request.set_attribute_template_option_code('ATOU_Option_1')
	request.set_code('ATOU_Option_1_Updated')
	request.set_prompt('ATOU_Option_1_Updated')
	request.set_price(1.13)
	request.set_cost(2.23)
	request.set_weight(3.34)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionUpdate)

	check = helper.get_attribute_template_option('ATOU_Template_1', 'ATOU_Attribute_1', 'ATOU_Option_1_Updated')

	assert check is not None
	assert check.get_code() == 'ATOU_Option_1_Updated'
	assert check.get_prompt() == 'ATOU_Option_1_Updated'
	assert check.get_price() == 1.13
	assert check.get_cost() == 2.23
	assert check.get_weight() == 3.34
