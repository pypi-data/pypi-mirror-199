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


def test_order_update_customer_information():
	"""
	Tests the Order_Update_Customer_Information API Call
	"""

	helper.provision_store('Order_Update_Customer_Information.xml')

	order_update_customer_information_test_update()


def order_update_customer_information_test_update():
	order = helper.get_order(678571)
	assert isinstance(order, merchantapi.model.Order)
	assert order.get_id() > 0

	request = merchantapi.request.OrderUpdateCustomerInformation(helper.init_client())

	request.set_order_id(order.get_id()) \
		.set_ship_first_name('Joe') \
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
		.set_bill_country('US')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderUpdateCustomerInformation)

	checkorder = helper.get_order(678571)

	assert isinstance(checkorder, merchantapi.model.Order)
	assert order.get_ship_first_name() != checkorder.get_ship_first_name()
	assert order.get_ship_last_name() != checkorder.get_ship_last_name()
	assert order.get_ship_phone() != checkorder.get_ship_phone()
	assert order.get_ship_fax() != checkorder.get_ship_fax()
	assert order.get_ship_city() != checkorder.get_ship_city()
	assert order.get_ship_state() != checkorder.get_ship_state()
	assert order.get_ship_zip() != checkorder.get_ship_zip()
	assert order.get_ship_country() != checkorder.get_ship_country()
	assert order.get_ship_address1() != checkorder.get_ship_address1()
	assert order.get_ship_address2() != checkorder.get_ship_address2()
	assert order.get_bill_first_name() != checkorder.get_bill_first_name()
	assert order.get_bill_last_name() != checkorder.get_bill_last_name()
	assert order.get_bill_phone() != checkorder.get_bill_phone()
	assert order.get_bill_fax() != checkorder.get_bill_fax()
	assert order.get_bill_city() != checkorder.get_bill_city()
	assert order.get_bill_state() != checkorder.get_bill_state()
	assert order.get_bill_zip() != checkorder.get_bill_zip()
	assert order.get_bill_country() != checkorder.get_bill_country()
	assert order.get_bill_address1() != checkorder.get_bill_address1()
	assert order.get_bill_address2() != checkorder.get_bill_address2()
