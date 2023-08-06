"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerAddress_Update_Residential. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customeraddress_update_residential
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerAddressUpdateResidential(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_address: merchantapi.model.CustomerAddress = None):
		"""
		CustomerAddressUpdateResidential Constructor.

		:param client: Client
		:param customer_address: CustomerAddress
		"""

		super().__init__(client)
		self.address_id = None
		self.customer_address_id = None
		self.residential = None
		if isinstance(customer_address, merchantapi.model.CustomerAddress):
			if customer_address.get_id():
				self.set_address_id(customer_address.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerAddress_Update_Residential'

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

	def get_residential(self) -> bool:
		"""
		Get Residential.

		:returns: bool
		"""

		return self.residential

	def set_address_id(self, address_id: int) -> 'CustomerAddressUpdateResidential':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: CustomerAddressUpdateResidential
		"""

		self.address_id = address_id
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'CustomerAddressUpdateResidential':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: CustomerAddressUpdateResidential
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_residential(self, residential: bool) -> 'CustomerAddressUpdateResidential':
		"""
		Set Residential.

		:param residential: bool
		:returns: CustomerAddressUpdateResidential
		"""

		self.residential = residential
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerAddressUpdateResidential':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerAddressUpdateResidential':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerAddressUpdateResidential(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.address_id is not None:
			data['Address_ID'] = self.address_id
		elif self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id

		if self.residential is not None:
			data['Residential'] = self.residential
		return data
