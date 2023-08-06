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


def test_customer_insert():
	"""
	Tests the Customer_Insert API Call
	"""

	helper.provision_store('Customer_Insert.xml')

	customer_insert_test_insertion()
	customer_insert_test_insertion_with_custom_fields()
	customer_insert_test_duplicate_customer()


def customer_insert_test_insertion():
	request = merchantapi.request.CustomerInsert(helper.init_client())

	request.set_customer_login('CustomerInsertTest_1') \
		.set_customer_password('P@ssw0rd') \
		.set_customer_password_email('test@coolcommerce.net') \
		.set_customer_bill_first_name('John') \
		.set_customer_bill_last_name('Doe') \
		.set_customer_bill_address1('1234 Some St') \
		.set_customer_bill_address2('Unit 100') \
		.set_customer_bill_city('San Diego') \
		.set_customer_bill_state('CA') \
		.set_customer_bill_zip('92009') \
		.set_customer_bill_country('USA') \
		.set_customer_bill_company('Miva Inc') \
		.set_customer_bill_phone('6191231234') \
		.set_customer_bill_fax('6191234321') \
		.set_customer_bill_email('test@coolcommerce.net') \
		.set_customer_ship_first_name('John') \
		.set_customer_ship_last_name('Deer') \
		.set_customer_ship_address1('4321 Some St') \
		.set_customer_ship_address2('Unit 200') \
		.set_customer_ship_city('San Diego') \
		.set_customer_ship_state('CA') \
		.set_customer_ship_zip('92009') \
		.set_customer_ship_phone('6191231234') \
		.set_customer_ship_fax('6191234321') \
		.set_customer_ship_email('test@coolcommerce.net') \
		.set_customer_ship_country('USA') \
		.set_customer_ship_company('Miva Inc')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerInsert)

	assert isinstance(response.get_customer(), merchantapi.model.Customer)
	assert response.get_customer().get_password_email() == 'test@coolcommerce.net'
	assert response.get_customer().get_bill_first_name() == 'John'
	assert response.get_customer().get_bill_last_name() == 'Doe'
	assert response.get_customer().get_bill_address1() == '1234 Some St'
	assert response.get_customer().get_bill_address2() == 'Unit 100'
	assert response.get_customer().get_bill_city() == 'San Diego'
	assert response.get_customer().get_bill_state() == 'CA'
	assert response.get_customer().get_bill_zip() == '92009'
	assert response.get_customer().get_bill_country() == 'USA'
	assert response.get_customer().get_bill_company() == 'Miva Inc'
	assert response.get_customer().get_bill_phone() == '6191231234'
	assert response.get_customer().get_bill_fax() == '6191234321'
	assert response.get_customer().get_bill_email() == 'test@coolcommerce.net'
	assert response.get_customer().get_ship_first_name() == 'John'
	assert response.get_customer().get_ship_last_name() == 'Deer'
	assert response.get_customer().get_ship_address1() == '4321 Some St'
	assert response.get_customer().get_ship_address2() == 'Unit 200'
	assert response.get_customer().get_ship_city() == 'San Diego'
	assert response.get_customer().get_ship_state() == 'CA'
	assert response.get_customer().get_ship_zip() == '92009'
	assert response.get_customer().get_ship_phone() == '6191231234'
	assert response.get_customer().get_ship_fax() == '6191234321'
	assert response.get_customer().get_ship_email() == 'test@coolcommerce.net'
	assert response.get_customer().get_ship_country() == 'USA'
	assert response.get_customer().get_ship_company() == 'Miva Inc'

	customer = response.get_customer()

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_id() == response.get_customer().get_id()


def customer_insert_test_insertion_with_custom_fields():
	request = merchantapi.request.CustomerInsert(helper.init_client())

	request.set_customer_login('CustomerInsertTest_2') \
		.set_customer_password('P@ssw0rd') \
		.set_customer_password_email('test@coolcommerce.net') \
		.set_customer_bill_first_name('John') \
		.set_customer_bill_last_name('Doe') \
		.set_customer_bill_address1('1234 Some St') \
		.set_customer_bill_address2('Unit 100') \
		.set_customer_bill_city('San Diego') \
		.set_customer_bill_state('CA') \
		.set_customer_bill_zip('92009') \
		.set_customer_bill_country('USA') \
		.set_customer_bill_company('Miva Inc') \
		.set_customer_bill_phone('6191231234') \
		.set_customer_bill_fax('6191234321') \
		.set_customer_bill_email('test@coolcommerce.net') \
		.set_customer_ship_first_name('John') \
		.set_customer_ship_last_name('Deer') \
		.set_customer_ship_address1('4321 Some St') \
		.set_customer_ship_address2('Unit 200') \
		.set_customer_ship_city('San Diego') \
		.set_customer_ship_state('CA') \
		.set_customer_ship_zip('92009') \
		.set_customer_ship_phone('6191231234') \
		.set_customer_ship_fax('6191234321') \
		.set_customer_ship_email('test@coolcommerce.net') \
		.set_customer_ship_country('USA') \
		.set_customer_ship_company('Miva Inc')

	request.get_custom_field_values()\
		.add_value('CustomerInsertTest_checkbox', 'True', 'customfields')\
		.add_value('CustomerInsertTest_imageupload', 'graphics/00000001/CustomerInsert.jpg', 'customfields')\
		.add_value('CustomerInsertTest_text', 'CustomerInsertTest_2', 'customfields')\
		.add_value('CustomerInsertTest_textarea', 'CustomerInsertTest_2', 'customfields')\
		.add_value('CustomerInsertTest_dropdown', 'Option2', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerInsert)

	customer = helper.get_customer('CustomerInsertTest_2')

	assert isinstance(customer, merchantapi.model.Customer)
	assert customer.get_password_email() == 'test@coolcommerce.net'
	assert customer.get_bill_first_name() == 'John'
	assert customer.get_bill_last_name() == 'Doe'
	assert customer.get_bill_address1() == '1234 Some St'
	assert customer.get_bill_address2() == 'Unit 100'
	assert customer.get_bill_city() == 'San Diego'
	assert customer.get_bill_state() == 'CA'
	assert customer.get_bill_zip() == '92009'
	assert customer.get_bill_country() == 'USA'
	assert customer.get_bill_company() == 'Miva Inc'
	assert customer.get_bill_phone() == '6191231234'
	assert customer.get_bill_fax() == '6191234321'
	assert customer.get_bill_email() == 'test@coolcommerce.net'
	assert customer.get_ship_first_name() == 'John'
	assert customer.get_ship_last_name() == 'Deer'
	assert customer.get_ship_address1() == '4321 Some St'
	assert customer.get_ship_address2() == 'Unit 200'
	assert customer.get_ship_city() == 'San Diego'
	assert customer.get_ship_state() == 'CA'
	assert customer.get_ship_zip() == '92009'
	assert customer.get_ship_phone() == '6191231234'
	assert customer.get_ship_fax() == '6191234321'
	assert customer.get_ship_email() == 'test@coolcommerce.net'
	assert customer.get_ship_country() == 'USA'
	assert customer.get_ship_company() == 'Miva Inc'

	assert isinstance(customer.get_custom_field_values(), merchantapi.model.CustomFieldValues)
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_checkbox', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_checkbox', 'customfields') == '1'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_imageupload', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_imageupload', 'customfields') == 'graphics/00000001/CustomerInsert.jpg'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_text', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_text', 'customfields') == 'CustomerInsertTest_2'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_textarea', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_textarea', 'customfields') == 'CustomerInsertTest_2'
	assert customer.get_custom_field_values().has_value('CustomerInsertTest_dropdown', 'customfields') is True
	assert customer.get_custom_field_values().get_value('CustomerInsertTest_dropdown', 'customfields') == 'Option2'


def customer_insert_test_duplicate_customer():
	request = merchantapi.request.CustomerInsert(helper.init_client())

	request.set_customer_login('CustomerInsertTest_Duplicate') \
		.set_customer_password('P@ssw0rd') \
		.set_customer_password_email('test@coolcommerce.net') \

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CustomerInsert)
