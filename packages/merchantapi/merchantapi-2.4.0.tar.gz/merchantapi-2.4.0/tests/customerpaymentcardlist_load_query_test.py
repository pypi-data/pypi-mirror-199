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


def test_customer_payment_card_list_load_query():
	"""
	Tests the CustomerPaymentCardList_Load_Query API Call
	"""

	helper.provision_store('MivaPay.xml')
	helper.provision_store('CustomerPaymentCardList_Load_Query.xml')

	customer_payment_card_list_load_query_test_list_load()


def customer_payment_card_list_load_query_test_list_load():
	cards = ['4788250000028291', '4055011111111111', '5454545454545454', '5405222222222226']
	lastfours = ['8291', '1111', '5454', '2226']

	mrequest = merchantapi.multicall.MultiCallRequest(helper.init_client())

	for card in cards:
		card_request = merchantapi.request.CustomerPaymentCardRegister(None)

		card_request.set_customer_login('CustomerPaymentCardList_Load_Query') \
			.set_first_name('John') \
			.set_last_name('Doe') \
			.set_card_type('MasterCard' if card[0] == 5 else 'Visa') \
			.set_card_number(card) \
			.set_expiration_month(8) \
			.set_expiration_year(2025) \
			.set_address1('1234 Test St') \
			.set_address2('Unit 123') \
			.set_city('San Diego') \
			.set_state('CA') \
			.set_zip('92009') \
			.set_country('USA')

		mrequest.add_request(card_request)

	mresponse = mrequest.send()

	helper.validate_response_success(mresponse, merchantapi.multicall.MultiCallResponse)

	assert isinstance(mresponse.get_responses(), list)

	for resp in mresponse.get_responses():
		helper.validate_response_success(resp, merchantapi.response.CustomerPaymentCardRegister)

	request = merchantapi.request.CustomerPaymentCardListLoadQuery(helper.init_client())

	request.set_customer_login('CustomerPaymentCardList_Load_Query')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerPaymentCardListLoadQuery)

	assert isinstance(response.get_customer_payment_cards(), list)
	assert len(response.get_customer_payment_cards()) == 4

	for card in response.get_customer_payment_cards():
		assert card.get_last_four() in lastfours
