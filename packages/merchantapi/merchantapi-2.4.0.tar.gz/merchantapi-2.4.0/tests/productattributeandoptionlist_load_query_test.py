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


def test_product_attribute_and_option_list_load_query():
	"""
	Tests the ProductAttributeAndOptionList_Load_Query API Call
	"""

	helper.provision_store('ProductAttributeAndOptionList_Load_Query.xml')

	product_attribute_and_option_list_load_query_test_list_load()


def product_attribute_and_option_list_load_query_test_list_load():
	request = merchantapi.request.ProductAttributeAndOptionListLoadQuery(helper.init_client())

	request.set_product_code('PATLLQ')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductAttributeAndOptionListLoadQuery)

	assert len(response.get_attributes()) == 2
	assert response.get_attributes()[0].get_product_id() > 0
	assert 'PATLLQ' in response.get_attributes()[0].get_code()
	assert response.get_attributes()[0].get_type() == 'template'
	assert isinstance(response.get_attributes()[0].get_template(), merchantapi.model.ProductAttributeListTemplate)
	assert response.get_attributes()[0].get_template().get_id() > 0

	assert response.get_attributes()[1].get_product_id() > 0
	assert 'PATLLQ' in response.get_attributes()[1].get_code()
	assert response.get_attributes()[1].get_type() == 'checkbox'
