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


def test_attribute_template_attribute_delete():
	"""
	Tests the AttributeTemplateAttribute_Delete API Call
	"""

	helper.provision_store('AttributeTemplateAttribute_Delete.xml')

	attribute_template_attribute_delete_test_deletion()


def attribute_template_attribute_delete_test_deletion():
	request = merchantapi.request.AttributeTemplateAttributeDelete(helper.init_client())

	request.set_attribute_template_code('ATAD_Template_1')
	request.set_attribute_template_attribute_code('ATAD_Attribute_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeDelete)

	check = helper.get_attribute_template_attribute('ATAD_Template_1', 'ATAD_Attribute_1')
	assert check is None
