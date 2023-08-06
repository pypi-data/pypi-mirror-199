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


def test_attribute_template_list_load_query():
	"""
	Tests the AttributeTemplateList_Load_Query API Call
	"""

	helper.provision_store('AttributeTemplateList_Load_Query.xml')

	attribute_template_list_load_query_test_list_load()


def attribute_template_list_load_query_test_list_load():
	request = merchantapi.request.AttributeTemplateListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'ATLLQ%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateListLoadQuery)

	assert len(response.get_attribute_templates()) > 0

	for a in response.get_attribute_templates():
		assert 'ATLLQ' in a.get_code()
