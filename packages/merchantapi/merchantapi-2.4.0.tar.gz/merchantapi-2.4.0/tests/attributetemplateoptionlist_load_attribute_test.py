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


def test_attribute_template_option_list_load_attribute():
	"""
	Tests the AttributeTemplateOptionList_Load_Attribute API Call
	"""

	helper.provision_store('AttributeTemplateOptionList_Load_Attribute.xml')

	attribute_template_option_list_load_attribute_test_list_load()


def attribute_template_option_list_load_attribute_test_list_load():
	request = merchantapi.request.AttributeTemplateOptionListLoadAttribute(helper.init_client())

	request.set_attribute_template_code('ATALLQ_Template_1')
	request.set_attribute_template_attribute_code('ATALLQ_Attribute_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionListLoadAttribute)

	assert len(response.get_attribute_template_options()) == 3

	for o in response.get_attribute_template_options():
		assert 'ATALLQ_Option_' in o.get_code()
