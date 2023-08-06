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


def test_customer_list_load_query():
	"""
	Tests the CustomerList_Load_Query API Call
	"""

	helper.provision_store('CustomerList_Load_Query.xml')
	helper.upload_image('graphics/CustomerListLoadQuery1.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery2.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery3.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery4.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery5.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery6.jpg')
	helper.upload_image('graphics/CustomerListLoadQuery7.jpg')

	customer_list_load_query_test_list_load()
	customer_list_load_query_test_list_load_with_custom_fields()


def customer_list_load_query_test_list_load():
	request = merchantapi.request.CustomerListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('login', 'CustomerListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerListLoadQuery)

	assert isinstance(response.get_customers(), list)
	assert len(response.get_customers()) == 7

	for i, customer in enumerate(response.get_customers()):
		assert isinstance(customer, merchantapi.model.Customer)
		assert customer.get_login() == 'CustomerListLoadQueryTest_%d' % int(i+1)


def customer_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.CustomerListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('login', 'CustomerListLoadQueryTest_%'))\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_checkbox')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_imageupload')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_text')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_textarea')\
		.add_on_demand_column('CustomField_Values:customfields:CustomerListLoadQueryTest_dropdown')\
		.set_sort('login', merchantapi.request.CustomerListLoadQuery.SORT_ASCENDING)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerListLoadQuery)

	assert isinstance(response.get_customers(), list)
	assert len(response.get_customers()) == 7

	for i, customer in enumerate(response.get_customers()):
		assert isinstance(customer, merchantapi.model.Customer)
		assert customer.get_login() == 'CustomerListLoadQueryTest_%d' % int(i+1)
		assert isinstance(customer.get_custom_field_values(), merchantapi.model.CustomFieldValues)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_checkbox', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_checkbox', 'customfields') == '1'
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_imageupload', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_imageupload', 'customfields') == 'graphics/00000001/CustomerListLoadQuery%d.jpg' % int(i+1)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_text', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_text', 'customfields') == 'CustomerListLoadQueryTest_%d' % int(i+1)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_textarea', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_textarea', 'customfields') == 'CustomerListLoadQueryTest_%d' % int(i+1)
		assert customer.get_custom_field_values().has_value('CustomerListLoadQueryTest_dropdown', 'customfields') is True
		assert customer.get_custom_field_values().get_value('CustomerListLoadQueryTest_dropdown', 'customfields') == 'Option%d' % int(i+1)
