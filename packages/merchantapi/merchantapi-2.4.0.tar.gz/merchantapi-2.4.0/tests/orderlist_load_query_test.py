"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
import json
from . import helper


def test_order_list_load_query():
	"""
	Tests the OrderList_Load_Query API Call
	"""

	helper.provision_store('OrderList_Load_Query.xml')
	helper.upload_image('graphics/OrderListLoadQuery1.jpg')
	helper.upload_image('graphics/OrderListLoadQuery2.jpg')
	helper.upload_image('graphics/OrderListLoadQuery3.jpg')
	helper.upload_image('graphics/OrderListLoadQuery4.jpg')
	helper.upload_image('graphics/OrderListLoadQuery5.jpg')
	helper.upload_image('graphics/OrderListLoadQuery6.jpg')
	helper.upload_image('graphics/OrderListLoadQuery7.jpg')

	order_list_load_query_test_list_load()
	order_list_load_query_test_list_load_with_custom_fields()
	order_list_load_query_test_list_load_detailed()
	order_list_load_query_test_list_load_MMAPI61()


def order_list_load_query_test_list_load():
	request = merchantapi.request.OrderListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().equal('cust_login', 'OrderListLoadQueryTest_Cust1')) \
		.add_on_demand_column('cust_login')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderListLoadQuery)

	assert isinstance(response.get_orders(), list)
	assert len(response.get_orders()) == 7

	for order in response.get_orders():
		assert isinstance(order, merchantapi.model.Order)
		assert order.get_customer_login() == 'OrderListLoadQueryTest_Cust1'
		assert order.get_id() in [678571, 678572, 678573, 678574, 678575, 678576, 678577]


def order_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.OrderListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().equal('cust_login', 'OrderListLoadQueryTest_Cust1')) \
		.set_on_demand_columns([
			'ship_method',
			'cust_login',
			'cust_pw_email',
			'business_title',
			'payment_module',
			'customer',
			'items',
			'charges',
			'coupons',
			'discounts',
			'payments',
			'notes'
		]) \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_checkbox') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_imageupload') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_text') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_textarea') \
		.add_on_demand_column('CustomField_Values:customfields:OrderListLoadQueryTest_dropdown')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderListLoadQuery)

	assert isinstance(response.get_orders(), list)
	assert len(response.get_orders()) == 7

	for i, order in enumerate(response.get_orders()):
		assert isinstance(order, merchantapi.model.Order)
		assert order.get_customer_login() == 'OrderListLoadQueryTest_Cust1'
		assert order.get_id() in [678571, 678572, 678573, 678574, 678575, 678576, 678577]
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_checkbox', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_checkbox', 'customfields') == '1'
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_imageupload', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_imageupload', 'customfields') == 'graphics/00000001/OrderListLoadQuery%d.jpg' % int(i+1)
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_text', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_text', 'customfields') == 'OrderListLoadQueryTest_%d' % int(i + 1)
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_textarea', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_textarea', 'customfields') == 'OrderListLoadQueryTest_%d' % int(i + 1)
		assert order.get_custom_field_values().has_value('OrderListLoadQueryTest_dropdown', 'customfields') is True
		assert order.get_custom_field_values().get_value('OrderListLoadQueryTest_dropdown', 'customfields') == 'Option%d' % int(i + 1)



def order_list_load_query_test_list_load_detailed():
	cod = helper.get_module('cod')
	assert cod is not None

	order = helper.get_order(678578)

	assert order is not None

	auth_response = helper.send_admin_request('Order_Authorize', {
        'Order_ID': 	order.get_id(),
        'Module_ID': 	cod['id'],
        'Amount': 		order.get_total(),
        'Module_Data': 	''
	})

	auth_response_data = json.loads(auth_response.content)

	assert auth_response_data is not None
	assert auth_response_data['success']

	order = helper.get_order(order.get_id())

	assert order is not None
    
	expected_charge_types = [ 'CUSTOM', 'SHIPPING', 'DISCOUNT', 'TAX' ]
	expected_discounts = [ 'OrderListLoadQueryTestDetailed_1', 'OrderListLoadQueryTestDetailed_2' ]

	assert len(order.get_items()) == 1
	assert order.get_items()[0].get_code() == 'OrderListLoadQueryTestDetailed_1'
	assert order.get_items()[0].get_name() == 'OrderListLoadQueryTestDetailed_1'
	assert order.get_items()[0].get_line_id() > 0
	assert order.get_items()[0].get_price() == 52.24
	assert order.get_items()[0].get_quantity() == 1
	assert order.get_items()[0].get_retail() == 5.0
	assert order.get_items()[0].get_order_id() == order.get_id()

	assert len(order.get_coupons()) == 1
	assert order.get_coupons()[0].get_code() == 'OrderListLoadQueryTestDetailed_1'
	assert order.get_coupons()[0].get_total() == 2.75
	assert order.get_coupons()[0].get_coupon_id() > 0
	assert order.get_coupons()[0].get_order_id() == order.get_id()

	assert len(order.get_charges()) == 4
	for charge in order.get_charges():
		assert charge.get_type() in expected_charge_types
		if charge.get_type() == 'CUSTOM':
			assert charge.get_amount() == 1.00
			assert charge.get_formatted_amount() == '$1.00'
			assert charge.get_charge_id() > 0
			assert charge.get_order_id() == order.get_id()


	assert len(order.get_discounts()) == 2
	for discount in order.get_discounts():
		assert discount.get_name() in expected_discounts
		assert discount.get_order_id() == order.get_id()

	assert len(order.get_payments()) == 1
	assert order.get_payments()[0].get_amount() == 60.73
	assert order.get_payments()[0].get_available() == 60.73
	assert order.get_payments()[0].get_formatted_amount() == '$60.73'
	assert order.get_payments()[0].get_formatted_available() == '$60.73'
	assert order.get_payments()[0].get_id() > 0
	assert order.get_payments()[0].get_order_id() == order.get_id()
	assert order.get_payments()[0].get_expires() == 0


def order_list_load_query_test_list_load_MMAPI61():
	order = helper.get_order(678578)

	assert order is not None
	assert len(order.get_items()) == 1
	assert len(order.get_items()[0].get_discounts()) > 0


def order_list_load_query_test_list_load_MMAPI88():
	order = helper.get_order(678578)

	assert order is not None
	assert len(order.get_items()) == 1
	assert order.get_items()[0].get_product_id() > 0
