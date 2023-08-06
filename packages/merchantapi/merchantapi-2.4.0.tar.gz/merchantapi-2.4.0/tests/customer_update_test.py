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


def test_customer_update():
	"""
	Tests the Customer_Update API Call
	"""

	helper.provision_store('Customer_Update.xml')

	customer_update_test_update()


def customer_update_test_update():
	request = merchantapi.request.CustomerUpdate(helper.init_client())

	request.set_edit_customer('CustomerUpdateTest_01') \
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

	helper.validate_response_success(response, merchantapi.response.CustomerUpdate)

	customer = helper.get_customer('CustomerUpdateTest_01')

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
