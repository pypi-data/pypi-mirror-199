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


def test_customer_payment_card_register():
	"""
	Tests the CustomerPaymentCard_Register API Call
	"""

	helper.provision_store('CustomerPaymentCard_Register.xml')

	customer_payment_card_register_test_register_card()


def customer_payment_card_register_test_register_card():
	request = merchantapi.request.CustomerPaymentCardRegister(helper.init_client())

	request.set_customer_login('CustomerPaymentCardRegisterTest')\
		.set_first_name('John')\
		.set_last_name('Doe')\
		.set_card_type('Visa')\
		.set_card_number('4111111111111111')\
		.set_expiration_month(8)\
		.set_expiration_year(2025)\
		.set_address1('1234 Test St')\
		.set_address2('Unit 123')\
		.set_city('San Diego')\
		.set_state('CA')\
		.set_zip('92009')\
		.set_country('US')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerPaymentCardRegister)

	card = response.get_customer_payment_card()

	assert isinstance(card, merchantapi.model.CustomerPaymentCard)
	assert card.get_token() is not None
	assert card.get_first_name() == 'John'
	assert card.get_last_name() == 'Doe'
	assert card.get_type() == 'Visa'
	assert card.get_last_four() == '1111'
	assert card.get_expiration_month() == 8
	assert card.get_expiration_year() == 2025
	assert card.get_address1() == '1234 Test St'
	assert card.get_address2() == 'Unit 123'
	assert card.get_city() == 'San Diego'
	assert card.get_state() == 'CA'
	assert card.get_zip() == '92009'
	assert card.get_country() == 'US'
