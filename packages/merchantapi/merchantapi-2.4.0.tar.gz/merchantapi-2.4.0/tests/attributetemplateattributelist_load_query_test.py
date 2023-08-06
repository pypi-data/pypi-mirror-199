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


def test_attribute_template_attribute_list_load_query():
	"""
	Tests the AttributeTemplateAttributeList_Load_Query API Call
	"""

	helper.provision_store('AttributeTemplateAttributeList_Load_Query.xml')

	attribute_template_attribute_list_load_query_test_list_load()


def attribute_template_attribute_list_load_query_test_list_load():
	request = merchantapi.request.AttributeTemplateAttributeListLoadQuery(helper.init_client())

	request.set_attribute_template_code('ATALLQ_Template_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeListLoadQuery)

	assert len(response.get_attribute_template_attributes()) > 0

	for a in response.get_attribute_template_attributes():
		assert 'ATALLQ' in a.get_code()
