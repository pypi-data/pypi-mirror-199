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


def test_attribute_template_update():
	"""
	Tests the AttributeTemplate_Update API Call
	"""

	helper.provision_store('AttributeTemplate_Update.xml')

	attribute_template_update_test_update()


def attribute_template_update_test_update():
	request = merchantapi.request.AttributeTemplateUpdate(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateUpdateTest_1')
	request.set_code('AttributeTemplateUpdateTest_1_Updated')
	request.set_prompt('AttributeTemplateUpdateTest_1_Updated')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateUpdate)

	check = helper.get_attribute_template('AttributeTemplateUpdateTest_1_Updated')

	assert check is not None
	assert check.get_code() == 'AttributeTemplateUpdateTest_1_Updated'
	assert check.get_prompt() == 'AttributeTemplateUpdateTest_1_Updated'
