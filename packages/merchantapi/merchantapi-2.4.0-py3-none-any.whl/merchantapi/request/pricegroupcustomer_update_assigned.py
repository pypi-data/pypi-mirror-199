"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroupCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcustomer_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCustomerUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.price_group_name = None
		self.edit_customer = None
		self.customer_id = None
		self.customer_login = None
		self.assigned = None
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCustomer_Update_Assigned'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

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

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_edit_customer(self, edit_customer: str) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_id(self, customer_id: int) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_customer_login(self, customer_login: str) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCustomerUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
