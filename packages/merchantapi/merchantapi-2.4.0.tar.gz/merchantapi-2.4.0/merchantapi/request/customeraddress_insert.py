"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerAddress_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerAddressInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerAddressInsert Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.customer_login = None
		self.description = None
		self.first_name = None
		self.last_name = None
		self.email = None
		self.phone = None
		self.fax = None
		self.company = None
		self.address1 = None
		self.address2 = None
		self.city = None
		self.state = None
		self.zip = None
		self.country = None
		self.residential = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Insert'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

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

	def get_email(self) -> str:
		"""
		Get Email.

		:returns: str
		"""

		return self.email

	def get_phone(self) -> str:
		"""
		Get Phone.

		:returns: str
		"""

		return self.phone

	def get_fax(self) -> str:
		"""
		Get Fax.

		:returns: str
		"""

		return self.fax

	def get_company(self) -> str:
		"""
		Get Company.

		:returns: str
		"""

		return self.company

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

	def get_residential(self) -> bool:
		"""
		Get Residential.

		:returns: bool
		"""

		return self.residential

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressInsert':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressInsert
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressInsert':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressInsert
		"""

		self.customer_login = customer_login
		return self

	def set_description(self, description: str) -> 'CustomerAddressInsert':
		"""
		Set Description.

		:param description: str
		:returns: CustomerAddressInsert
		"""

		self.description = description
		return self

	def set_first_name(self, first_name: str) -> 'CustomerAddressInsert':
		"""
		Set FirstName.

		:param first_name: str
		:returns: CustomerAddressInsert
		"""

		self.first_name = first_name
		return self

	def set_last_name(self, last_name: str) -> 'CustomerAddressInsert':
		"""
		Set LastName.

		:param last_name: str
		:returns: CustomerAddressInsert
		"""

		self.last_name = last_name
		return self

	def set_email(self, email: str) -> 'CustomerAddressInsert':
		"""
		Set Email.

		:param email: str
		:returns: CustomerAddressInsert
		"""

		self.email = email
		return self

	def set_phone(self, phone: str) -> 'CustomerAddressInsert':
		"""
		Set Phone.

		:param phone: str
		:returns: CustomerAddressInsert
		"""

		self.phone = phone
		return self

	def set_fax(self, fax: str) -> 'CustomerAddressInsert':
		"""
		Set Fax.

		:param fax: str
		:returns: CustomerAddressInsert
		"""

		self.fax = fax
		return self

	def set_company(self, company: str) -> 'CustomerAddressInsert':
		"""
		Set Company.

		:param company: str
		:returns: CustomerAddressInsert
		"""

		self.company = company
		return self

	def set_address1(self, address1: str) -> 'CustomerAddressInsert':
		"""
		Set Address1.

		:param address1: str
		:returns: CustomerAddressInsert
		"""

		self.address1 = address1
		return self

	def set_address2(self, address2: str) -> 'CustomerAddressInsert':
		"""
		Set Address2.

		:param address2: str
		:returns: CustomerAddressInsert
		"""

		self.address2 = address2
		return self

	def set_city(self, city: str) -> 'CustomerAddressInsert':
		"""
		Set City.

		:param city: str
		:returns: CustomerAddressInsert
		"""

		self.city = city
		return self

	def set_state(self, state: str) -> 'CustomerAddressInsert':
		"""
		Set State.

		:param state: str
		:returns: CustomerAddressInsert
		"""

		self.state = state
		return self

	def set_zip(self, zip: str) -> 'CustomerAddressInsert':
		"""
		Set Zip.

		:param zip: str
		:returns: CustomerAddressInsert
		"""

		self.zip = zip
		return self

	def set_country(self, country: str) -> 'CustomerAddressInsert':
		"""
		Set Country.

		:param country: str
		:returns: CustomerAddressInsert
		"""

		self.country = country
		return self

	def set_residential(self, residential: bool) -> 'CustomerAddressInsert':
		"""
		Set Residential.

		:param residential: bool
		:returns: CustomerAddressInsert
		"""

		self.residential = residential
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.description is not None:
			data['Description'] = self.description
		if self.first_name is not None:
			data['FirstName'] = self.first_name
		if self.last_name is not None:
			data['LastName'] = self.last_name
		if self.email is not None:
			data['Email'] = self.email
		if self.phone is not None:
			data['Phone'] = self.phone
		if self.fax is not None:
			data['Fax'] = self.fax
		if self.company is not None:
			data['Company'] = self.company
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
		if self.residential is not None:
			data['Residential'] = self.residential
		return data
