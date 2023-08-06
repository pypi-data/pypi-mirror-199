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


def test_option_list_load_attribute():
	"""
	Tests the OptionList_Load_Attribute API Call
	"""

	helper.provision_store('OptionList_Load_Attribute.xml')

	option_list_load_attribute_test_load()


def option_list_load_attribute_test_load():
	request = merchantapi.request.OptionListLoadAttribute(helper.init_client())

	request.set_product_code('OptionListLoadAttributeTest_1')
	request.set_attribute_code('OptionListLoadAttributeTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionListLoadAttribute)

	assert len(response.get_product_options()) == 2
	assert response.get_product_options()[0].get_code() == 'OptionListLoadAttributeTest_1'
	assert response.get_product_options()[1].get_code() == 'OptionListLoadAttributeTest_2'
