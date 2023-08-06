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


def test_attribute_template_product_update_assigned():
	"""
	Tests the AttributeTemplateProduct_Update_Assigned API Call
	"""

	helper.provision_store('AttributeTemplateProduct_Update_Assigned.xml')

	attribute_template_product_update_assigned_test_assignment()
	attribute_template_product_update_assigned_test_unassignment()


def attribute_template_product_update_assigned_test_assignment():
	request = merchantapi.request.AttributeTemplateProductUpdateAssigned(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_1')
	request.set_product_code('AttributeTemplateProductUpdateAssignedTest_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateProductUpdateAssigned)

	check_request = merchantapi.request.AttributeTemplateProductListLoadQuery(helper.init_client())
	check_request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_1')
	check_request.set_filters(check_request.filter_expression().equal('code', 'AttributeTemplateProductUpdateAssignedTest_1'))
	check_request.set_assigned(True)
	check_request.set_unassigned(False)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.AttributeTemplateProductListLoadQuery)

	assert len(check_response.get_attribute_template_products()) == 1
	assert check_response.get_attribute_template_products()[0].get_assigned() is True


def attribute_template_product_update_assigned_test_unassignment():
	request = merchantapi.request.AttributeTemplateProductUpdateAssigned(helper.init_client())

	request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_2')
	request.set_product_code('AttributeTemplateProductUpdateAssignedTest_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateProductUpdateAssigned)

	check_request = merchantapi.request.AttributeTemplateProductListLoadQuery(helper.init_client())
	check_request.set_attribute_template_code('AttributeTemplateProductUpdateAssignedTest_2')
	check_request.set_filters(check_request.filter_expression().equal('code', 'AttributeTemplateProductUpdateAssignedTest_2'))
	check_request.set_assigned(False)
	check_request.set_unassigned(True)

	check_response = check_request.send()

	helper.validate_response_success(check_response, merchantapi.response.AttributeTemplateProductListLoadQuery)

	assert len(check_response.get_attribute_template_products()) == 1
	assert check_response.get_attribute_template_products()[0].get_assigned() is False
