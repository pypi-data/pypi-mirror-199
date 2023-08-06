"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerSubscriptionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customersubscriptionlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import SubscriptionListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerSubscriptionListLoadQuery(SubscriptionListLoadQuery):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerSubscriptionListLoadQuery Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())


			if customer.get_custom_field_values():
				self.set_custom_field_values(customer.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerSubscriptionList_Load_Query'

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

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_customer_id(self, customer_id: int) -> 'CustomerSubscriptionListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerSubscriptionListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerSubscriptionListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerSubscriptionListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerSubscriptionListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerSubscriptionListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CustomerSubscriptionListLoadQuery':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CustomerSubscriptionListLoadQuery
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerSubscriptionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerSubscriptionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerSubscriptionListLoadQuery(self, http_response, data)

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

		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
