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


def test_attribute_template_option_set_default():
	"""
	Tests the AttributeTemplateOption_Set_Default API Call
	"""

	helper.provision_store('AttributeTemplateOption_Set_Default.xml')

	attribute_template_option_set_default_test_set_default()


def attribute_template_option_set_default_test_set_default():
	request = merchantapi.request.AttributeTemplateOptionSetDefault(helper.init_client())

	request.set_attribute_template_code('ATOSD_Template_1')
	request.set_attribute_template_attribute_code('ATOSD_Attribute_1')
	request.set_attribute_template_option_code('ATOSD_Option_2')
	request.set_attribute_template_option_default(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionSetDefault)

	checkA = helper.get_attribute_template_attribute('ATOSD_Template_1', 'ATOSD_Attribute_1')
	checkO = helper.get_attribute_template_option('ATOSD_Template_1', 'ATOSD_Attribute_1', 'ATOSD_Option_2')

	assert checkA is not None
	assert checkO is not None
	assert checkA.get_default_id() == checkO.get_id()
