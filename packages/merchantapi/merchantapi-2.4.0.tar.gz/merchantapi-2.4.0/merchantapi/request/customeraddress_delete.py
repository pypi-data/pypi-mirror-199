"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerAddress_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerAddressDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_address: merchantapi.model.CustomerAddress = None):
		"""
		CustomerAddressDelete Constructor.

		:param client: Client
		:param customer_address: CustomerAddress
		"""

		super().__init__(client)
		self.address_id = None
		self.customer_address_id = None
		self.customer_id = None
		self.customer_login = None
		self.edit_customer = None
		if isinstance(customer_address, merchantapi.model.CustomerAddress):
			if customer_address.get_customer_id():
				self.set_customer_id(customer_address.get_customer_id())

			if customer_address.get_id():
				self.set_address_id(customer_address.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Delete'

	def get_address_id(self) -> int:
		"""
		Get Address_ID.

		:returns: int
		"""

		return self.address_id

	def get_customer_address_id(self) -> int:
		"""
		Get CustomerAddress_ID.

		:returns: int
		"""

		return self.customer_address_id

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

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def set_address_id(self, address_id: int) -> 'CustomerAddressDelete':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: CustomerAddressDelete
		"""

		self.address_id = address_id
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'CustomerAddressDelete':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: CustomerAddressDelete
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressDelete':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressDelete
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressDelete':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressDelete
		"""

		self.customer_login = customer_login
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerAddressDelete':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerAddressDelete
		"""

		self.edit_customer = edit_customer
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressDelete(self, http_response, data)

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
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer

		if self.address_id is not None:
			data['Address_ID'] = self.address_id
		elif self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id

		return data
