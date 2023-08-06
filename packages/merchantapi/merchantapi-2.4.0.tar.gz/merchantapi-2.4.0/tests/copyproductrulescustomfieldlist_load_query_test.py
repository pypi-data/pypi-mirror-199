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


def test_copyproductrulescustomfieldlist_load_query():
	"""
	Tests the CopyProductRulesCustomFieldList_Load_Query API Call
	"""

	helper.provision_store('CopyProductRulesCustomFieldList_Load_Query.xml')

	copyproductrulescustomfieldlist_load_query_test_listload_all()
	copyproductrulescustomfieldlist_load_query_test_listload_assigned()
	copyproductrulescustomfieldlist_load_query_test_listload_unassigned()


def copyproductrulescustomfieldlist_load_query_test_listload_all():
	request = merchantapi.request.CopyProductRulesCustomFieldListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesCustomFieldList_Load_Query_1')
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().equal('field_name', 'CopyProductRulesCustomFieldList_Load_Query')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesCustomFieldListLoadQuery)

	assert len(response.get_copy_product_rules_custom_fields()) == 2
	assert response.get_copy_product_rules_custom_fields()[0].get_field_code() == 'CopyProductRulesCustomFieldList_Load_Query_1'
	assert response.get_copy_product_rules_custom_fields()[1].get_field_code() == 'CopyProductRulesCustomFieldList_Load_Query_2'


def copyproductrulescustomfieldlist_load_query_test_listload_assigned():
	request = merchantapi.request.CopyProductRulesCustomFieldListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesCustomFieldList_Load_Query_1')
	request.set_assigned(True)
	request.set_unassigned(False)
	request.get_filters().equal('field_name', 'CopyProductRulesCustomFieldList_Load_Query')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesCustomFieldListLoadQuery)

	assert len(response.get_copy_product_rules_custom_fields()) == 1
	assert response.get_copy_product_rules_custom_fields()[0].get_field_code() == 'CopyProductRulesCustomFieldList_Load_Query_1'

def copyproductrulescustomfieldlist_load_query_test_listload_unassigned():
	request = merchantapi.request.CopyProductRulesCustomFieldListLoadQuery(helper.init_client())

	request.set_copy_product_rules_name('CopyProductRulesCustomFieldList_Load_Query_1')
	request.set_assigned(False)
	request.set_unassigned(True)
	request.get_filters().equal('field_name', 'CopyProductRulesCustomFieldList_Load_Query')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CopyProductRulesCustomFieldListLoadQuery)

	assert len(response.get_copy_product_rules_custom_fields()) == 1
	assert response.get_copy_product_rules_custom_fields()[0].get_field_code() == 'CopyProductRulesCustomFieldList_Load_Query_2'