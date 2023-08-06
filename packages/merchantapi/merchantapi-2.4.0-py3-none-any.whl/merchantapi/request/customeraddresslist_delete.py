"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerAddressList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddresslist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerAddressListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerAddressListDelete Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.customer_login = None
		self.edit_customer = None
		self.customer_address_ids = []
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_customer_login(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddressList_Delete'

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

	def get_customer_address_ids(self):
		"""
		Get CustomerAddress_IDs.

		:returns: list
		"""

		return self.customer_address_ids

	def set_customer_id(self, customer_id: int) -> 'CustomerAddressListDelete':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerAddressListDelete
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerAddressListDelete':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerAddressListDelete
		"""

		self.customer_login = customer_login
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerAddressListDelete':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerAddressListDelete
		"""

		self.edit_customer = edit_customer
		return self
	
	def add_customer_address_id(self, customer_address_id) -> 'CustomerAddressListDelete':
		"""
		Add CustomerAddress_IDs.

		:param customer_address_id: int
		:returns: {CustomerAddressListDelete}
		"""

		self.customer_address_ids.append(customer_address_id)
		return self

	def add_customer_address(self, customer_address: merchantapi.model.CustomerAddress) -> 'CustomerAddressListDelete':
		"""
		Add CustomerAddress model.

		:param customer_address: CustomerAddress
		:raises Exception:
		:returns: CustomerAddressListDelete
		"""
		if not isinstance(customer_address, merchantapi.model.CustomerAddress):
			raise Exception('Expected an instance of CustomerAddress')

		if customer_address.get_id():
			self.customer_address_ids.append(customer_address.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressListDelete(self, http_response, data)

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

		data['CustomerAddress_IDs'] = self.customer_address_ids
		return data
