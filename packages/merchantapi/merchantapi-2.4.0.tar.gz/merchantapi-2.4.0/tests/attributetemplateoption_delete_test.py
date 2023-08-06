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


def test_attribute_template_option_delete():
	"""
	Tests the AttributeTemplateOption_Delete API Call
	"""

	helper.provision_store('AttributeTemplateOption_Delete.xml')

	attribute_template_option_delete_test_deletion()


def attribute_template_option_delete_test_deletion():
	request = merchantapi.request.AttributeTemplateOptionDelete(helper.init_client())

	request.set_attribute_template_code('ATOD_Template_1')
	request.set_attribute_template_attribute_code('ATOD_Attribute_1')
	request.set_attribute_template_option_code('ATOD_Option_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionDelete)

	check = helper.get_attribute_template_option('ATOD_Template_1', 'ATOD_Attribute_1', 'ATOD_Option_1')

	assert check is None
