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


def test_order_create():
	"""
	Tests the Order_Create API Call
	"""

	helper.provision_store('Order_Create.xml')

	order_create_test_creation()
	order_create_test_creation_with_customer()
	order_create_test_invalid_customer()
	order_create_test_with_customer_info()
	order_create_test_creation_with_everything()


def order_create_test_creation():
	request = merchantapi.request.OrderCreate(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0


def order_create_test_creation_with_customer():
	request = merchantapi.request.OrderCreate(helper.init_client())

	request.set_customer_login('OrderCreateTest_Cust_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert response.get_order().get_customer_id() > 0


def order_create_test_invalid_customer():
	request = merchantapi.request.OrderCreate(helper.init_client())

	request.set_customer_login('InvalidCustomer')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.OrderCreate)


def order_create_test_with_customer_info():
	request = merchantapi.request.OrderCreate(helper.init_client())

	request.set_ship_first_name('Joe') \
		.set_ship_last_name('Dirt') \
		.set_ship_email('test@coolcommerce.net') \
		.set_ship_phone('6191231234') \
		.set_ship_fax('6191234321') \
		.set_ship_company('Dierte Inc') \
		.set_ship_address1('1234 Test Ave') \
		.set_ship_address2('Unit 100') \
		.set_ship_city('San Diego') \
		.set_ship_state('CA') \
		.set_ship_zip('92009') \
		.set_ship_country('USA') \
		.set_ship_residential(True) \
		.set_bill_first_name('Joe') \
		.set_bill_last_name('Dirt') \
		.set_bill_email('test@coolcommerce.net') \
		.set_bill_phone('6191231234') \
		.set_bill_fax('6191234321') \
		.set_bill_company('Dierte Inc') \
		.set_bill_address1('1234 Test Ave') \
		.set_bill_address2('Unit 100') \
		.set_bill_city('San Diego') \
		.set_bill_state('CA') \
		.set_bill_zip('92009') \
		.set_bill_country('US') \
		.set_calculate_charges(False) \
		.set_trigger_fulfillment_modules(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0
	assert response.get_order().get_ship_first_name() == 'Joe'
	assert response.get_order().get_ship_last_name() == 'Dirt'
	assert response.get_order().get_ship_email() == 'test@coolcommerce.net'
	assert response.get_order().get_ship_phone() == '6191231234'
	assert response.get_order().get_ship_fax() == '6191234321'
	assert response.get_order().get_ship_company() == 'Dierte Inc'
	assert response.get_order().get_ship_address1() == '1234 Test Ave'
	assert response.get_order().get_ship_address2() == 'Unit 100'
	assert response.get_order().get_ship_city() == 'San Diego'
	assert response.get_order().get_ship_state() == 'CA'
	assert response.get_order().get_ship_zip() == '92009'
	assert response.get_order().get_ship_country() == 'USA'
	assert response.get_order().get_ship_residential() is True
	assert response.get_order().get_bill_first_name() == 'Joe'
	assert response.get_order().get_bill_last_name() == 'Dirt'
	assert response.get_order().get_bill_email() == 'test@coolcommerce.net'
	assert response.get_order().get_bill_phone() == '6191231234'
	assert response.get_order().get_bill_fax() == '6191234321'
	assert response.get_order().get_bill_company() == 'Dierte Inc'
	assert response.get_order().get_bill_address1() == '1234 Test Ave'
	assert response.get_order().get_bill_address2() == 'Unit 100'
	assert response.get_order().get_bill_city() == 'San Diego'
	assert response.get_order().get_bill_state() == 'CA'
	assert response.get_order().get_bill_zip() == '92009'
	assert response.get_order().get_bill_country() == 'US'


def order_create_test_creation_with_everything():
	request = merchantapi.request.OrderCreate(helper.init_client())
	charge = merchantapi.model.OrderCharge()
	item = merchantapi.model.OrderItem()
	item_opt = merchantapi.model.OrderItemOption()
	product = merchantapi.model.OrderProduct()
	prod_attr = merchantapi.model.OrderProductAttribute()

	charge.set_description('foo') \
		.set_amount(29.99) \
		.set_type('API')

	item.set_name('Test Custom Line') \
		.set_code('CUSTOM_LINE') \
		.set_price(15.00) \
		.set_quantity(1)

	item_opt.set_attribute_code('option')\
		.set_value('option_data') \
		.set_price(5.00) \
		.set_weight(1.00)

	item.add_option(item_opt)

	product.set_code('OrderCreateTest_Prod_3') \
		.set_quantity(1)

	prod_attr.set_code('color') \
		.set_value('red')

	product.add_attribute(prod_attr)

	request.set_customer_login('OrderCreateTest_Cust_2') \
		.set_calculate_charges(False) \
		.set_trigger_fulfillment_modules(False) \
		.add_charge(charge) \
		.add_item(item) \
		.add_product(product)

	request.get_custom_field_values() \
		.add_value('OrderCreateTest_1', 'foo') \
		.add_value('OrderCreateTest_2', 'bar') \
		.add_value('OrderCreateTest_3', 'baz', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderCreate)

	assert isinstance(response.get_order(), merchantapi.model.Order)
	assert response.get_order().get_id() > 0

	order = helper.get_order(response.get_order().get_id())

	assert isinstance(order, merchantapi.model.Order)
	assert order.get_id() == response.get_order().get_id()
	assert order.get_customer_login() == 'OrderCreateTest_Cust_2'
	assert isinstance(order.get_items(), list)
	assert len(order.get_items()) == 2

	item1 = order.get_items()[0]

	assert item1.get_code() == 'CUSTOM_LINE'
	assert item1.get_price() == 15.00
	assert isinstance(item1.get_options(), list)
	assert len(item1.get_options()) == 1

	item1_option1 = item1.get_options()[0]

	assert item1_option1.get_attribute_code() == 'option'
	assert item1_option1.get_value() == 'option_data'
	assert item1_option1.get_price() == 5.00
	assert item1_option1.get_weight() == 1.00

	item2 = order.get_items()[1]

	assert item2.get_code() == 'OrderCreateTest_Prod_3'
	assert item2.get_price() == 4.00
	assert isinstance(item2.get_options(), list)
	assert len(item2.get_options()) == 1

	item2_option1 = item2.get_options()[0]

	assert item2_option1.get_attribute_code() == 'color'
	assert item2_option1.get_value() == 'red'
	assert item2_option1.get_price() == 5.99
	assert item2_option1.get_weight() == 1.21

	assert isinstance(order.get_charges(), list)
	assert len(order.get_charges()) == 1

	charge = order.get_charges()[0]

	assert isinstance(charge, merchantapi.model.OrderCharge)
	assert charge.get_description() == 'foo'
	assert charge.get_amount() == 29.99
	assert charge.get_type() == 'API'

	assert isinstance(order.get_customer(), merchantapi.model.Customer)
	assert order.get_customer().get_login() == 'OrderCreateTest_Cust_2'
	assert isinstance(order.get_custom_field_values(), merchantapi.model.CustomFieldValues)
	assert order.get_custom_field_values().get_value('OrderCreateTest_1') == 'foo'
	assert order.get_custom_field_values().get_value('OrderCreateTest_2') == 'bar'
	assert order.get_custom_field_values().get_value('OrderCreateTest_3') == 'baz'
