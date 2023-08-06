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


def test_pagelist_load_query():
	"""
	Tests the PageList_Load_Query API Call
	"""

	helper.provision_store('PageList_Load_Query.xml')

	pagelist_load_query_test_listload()


def pagelist_load_query_test_listload():
	request = merchantapi.request.PageListLoadQuery(helper.init_client())

	request.get_filters().like('code', 'PLLQ_%')
	request.set_on_demand_columns(request.get_available_on_demand_columns())
	
	request.add_on_demand_column('CustomField_Values:customfields:PLLQ_Test_checkbox') \
		.add_on_demand_column('CustomField_Values:customfields:PLLQ_Test_imageupload') \
		.add_on_demand_column('CustomField_Values:customfields:PLLQ_Test_text') \
		.add_on_demand_column('CustomField_Values:customfields:PLLQ_Test_textarea') \
		.add_on_demand_column('CustomField_Values:customfields:PLLQ_Test_dropdown') 

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageListLoadQuery)

	assert len(response.get_pages()) == 6

	for i, page in enumerate(response.get_pages()):
		assert page.get_code() == 'PLLQ_' + str(i+1)
		assert page.get_name() == 'PLLQ_' + str(i+1) + ' Page'
		assert page.get_title() == 'PLLQ_' + str(i+1) + ' Title'
		assert page.get_code() == 'PLLQ_' + str(i+1)		
		assert page.get_custom_field_values() is not None
		assert page.get_custom_field_values().has_value('PLLQ_Test_checkbox', 'customfields') is True
		assert page.get_custom_field_values().has_value('PLLQ_Test_imageupload', 'customfields') is True
		assert page.get_custom_field_values().has_value('PLLQ_Test_text', 'customfields') is True
		assert page.get_custom_field_values().has_value('PLLQ_Test_textarea', 'customfields') is True
		assert page.get_custom_field_values().has_value('PLLQ_Test_dropdown', 'customfields') is True

		assert page.get_notes() == 'Original'
		assert len(page.get_uris()) > 0
		assert len(page.get_url()) > 0
		assert page.get_source() == 'PLLQ_' + str(i+1)	+ ' Template'
		for uri in page.get_uris():
			assert isinstance(uri, merchantapi.model.Uri)