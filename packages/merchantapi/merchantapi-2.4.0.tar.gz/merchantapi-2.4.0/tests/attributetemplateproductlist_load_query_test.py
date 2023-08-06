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


def test_attribute_template_product_list_load_query():
	"""
	Tests the AttributeTemplateProductList_Load_Query API Call
	"""

	helper.provision_store('AttributeTemplateProductList_Load_Query.xml')

	attribute_template_product_list_load_query_test_list_load()


def attribute_template_product_list_load_query_test_list_load():
	request = merchantapi.request.AttributeTemplateProductListLoadQuery(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateProductListTemplate')
	request.set_assigned(True)
	request.set_unassigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateProductListLoadQuery)

	assert len(response.get_attribute_template_products()) > 0

	for p in response.get_attribute_template_products():
		assert 'AttributeTemplateProduct' in p.get_code()
