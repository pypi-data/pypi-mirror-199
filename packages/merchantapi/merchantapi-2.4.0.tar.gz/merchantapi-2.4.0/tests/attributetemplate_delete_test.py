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


def test_attribute_template_delete():
	"""
	Tests the AttributeTemplate_Delete API Call
	"""

	helper.provision_store('AttributeTemplate_Delete.xml')

	attribute_template_delete_test_deletion()


def attribute_template_delete_test_deletion():
	request = merchantapi.request.AttributeTemplateDelete(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateDeleteTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateDelete)

	check = helper.get_attribute_template('AttributeTemplateDeleteTest_1')

	assert check is None
