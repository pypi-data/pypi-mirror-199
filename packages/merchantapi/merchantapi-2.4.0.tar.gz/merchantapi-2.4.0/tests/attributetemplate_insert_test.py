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


def test_attribute_template_insert():
	"""
	Tests the AttributeTemplate_Insert API Call
	"""

	helper.provision_store('AttributeTemplate_Insert.xml')

	attribute_template_insert_test_insertion()


def attribute_template_insert_test_insertion():
	request = merchantapi.request.AttributeTemplateInsert(helper.init_client())

	request.set_code('AttributeTemplateInsertTest_1')
	request.set_prompt('AttributeTemplateInsertTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateInsert)

	assert isinstance(response.get_attribute_template(), merchantapi.model.AttributeTemplate)
	assert response.get_attribute_template().get_code() == 'AttributeTemplateInsertTest_1'
	assert response.get_attribute_template().get_prompt() == 'AttributeTemplateInsertTest_1'

	check = helper.get_attribute_template('AttributeTemplateInsertTest_1')

	assert check is not None
	assert check.get_id() == response.get_attribute_template().get_id()
