"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerPaymentCard_Register. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customerpaymentcard_register
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerPaymentCardRegister(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerPaymentCardRegister Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.first_name = None
		self.last_name = None
		self.card_type = None
		self.card_number = None
		self.expiration_month = None
		self.expiration_year = None
		self.address1 = None
		self.address2 = None
		self.city = None
		self.state = None
		self.zip = None
		self.country = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerPaymentCard_Register'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_first_name(self) -> str:
		"""
		Get FirstName.

		:returns: str
		"""

		return self.first_name

	def get_last_name(self) -> str:
		"""
		Get LastName.

		:returns: str
		"""

		return self.last_name

	def get_card_type(self) -> str:
		"""
		Get CardType.

		:returns: str
		"""

		return self.card_type

	def get_card_number(self) -> str:
		"""
		Get CardNumber.

		:returns: str
		"""

		return self.card_number

	def get_expiration_month(self) -> int:
		"""
		Get ExpirationMonth.

		:returns: int
		"""

		return self.expiration_month

	def get_expiration_year(self) -> int:
		"""
		Get ExpirationYear.

		:returns: int
		"""

		return self.expiration_year

	def get_address1(self) -> str:
		"""
		Get Address1.

		:returns: str
		"""

		return self.address1

	def get_address2(self) -> str:
		"""
		Get Address2.

		:returns: str
		"""

		return self.address2

	def get_city(self) -> str:
		"""
		Get City.

		:returns: str
		"""

		return self.city

	def get_state(self) -> str:
		"""
		Get State.

		:returns: str
		"""

		return self.state

	def get_zip(self) -> str:
		"""
		Get Zip.

		:returns: str
		"""

		return self.zip

	def get_country(self) -> str:
		"""
		Get Country.

		:returns: str
		"""

		return self.country

	def set_customer_id(self, customer_id: int) -> 'CustomerPaymentCardRegister':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerPaymentCardRegister
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerPaymentCardRegister
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerPaymentCardRegister
		"""

		self.customer_login = customer_login
		return self

	def set_first_name(self, first_name: str) -> 'CustomerPaymentCardRegister':
		"""
		Set FirstName.

		:param first_name: str
		:returns: CustomerPaymentCardRegister
		"""

		self.first_name = first_name
		return self

	def set_last_name(self, last_name: str) -> 'CustomerPaymentCardRegister':
		"""
		Set LastName.

		:param last_name: str
		:returns: CustomerPaymentCardRegister
		"""

		self.last_name = last_name
		return self

	def set_card_type(self, card_type: str) -> 'CustomerPaymentCardRegister':
		"""
		Set CardType.

		:param card_type: str
		:returns: CustomerPaymentCardRegister
		"""

		self.card_type = card_type
		return self

	def set_card_number(self, card_number: str) -> 'CustomerPaymentCardRegister':
		"""
		Set CardNumber.

		:param card_number: str
		:returns: CustomerPaymentCardRegister
		"""

		self.card_number = card_number
		return self

	def set_expiration_month(self, expiration_month: int) -> 'CustomerPaymentCardRegister':
		"""
		Set ExpirationMonth.

		:param expiration_month: int
		:returns: CustomerPaymentCardRegister
		"""

		self.expiration_month = expiration_month
		return self

	def set_expiration_year(self, expiration_year: int) -> 'CustomerPaymentCardRegister':
		"""
		Set ExpirationYear.

		:param expiration_year: int
		:returns: CustomerPaymentCardRegister
		"""

		self.expiration_year = expiration_year
		return self

	def set_address1(self, address1: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Address1.

		:param address1: str
		:returns: CustomerPaymentCardRegister
		"""

		self.address1 = address1
		return self

	def set_address2(self, address2: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Address2.

		:param address2: str
		:returns: CustomerPaymentCardRegister
		"""

		self.address2 = address2
		return self

	def set_city(self, city: str) -> 'CustomerPaymentCardRegister':
		"""
		Set City.

		:param city: str
		:returns: CustomerPaymentCardRegister
		"""

		self.city = city
		return self

	def set_state(self, state: str) -> 'CustomerPaymentCardRegister':
		"""
		Set State.

		:param state: str
		:returns: CustomerPaymentCardRegister
		"""

		self.state = state
		return self

	def set_zip(self, zip: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Zip.

		:param zip: str
		:returns: CustomerPaymentCardRegister
		"""

		self.zip = zip
		return self

	def set_country(self, country: str) -> 'CustomerPaymentCardRegister':
		"""
		Set Country.

		:param country: str
		:returns: CustomerPaymentCardRegister
		"""

		self.country = country
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerPaymentCardRegister':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerPaymentCardRegister':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerPaymentCardRegister(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.first_name is not None:
			data['FirstName'] = self.first_name
		if self.last_name is not None:
			data['LastName'] = self.last_name
		if self.card_type is not None:
			data['CardType'] = self.card_type
		if self.card_number is not None:
			data['CardNumber'] = self.card_number
		if self.expiration_month is not None:
			data['ExpirationMonth'] = self.expiration_month
		if self.expiration_year is not None:
			data['ExpirationYear'] = self.expiration_year
		if self.address1 is not None:
			data['Address1'] = self.address1
		if self.address2 is not None:
			data['Address2'] = self.address2
		if self.city is not None:
			data['City'] = self.city
		if self.state is not None:
			data['State'] = self.state
		if self.zip is not None:
			data['Zip'] = self.zip
		if self.country is not None:
			data['Country'] = self.country
		return data
