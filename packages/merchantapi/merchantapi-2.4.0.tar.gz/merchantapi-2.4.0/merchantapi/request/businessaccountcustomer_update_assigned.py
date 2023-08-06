"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BusinessAccountCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountcustomer_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BusinessAccountCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, business_account: merchantapi.model.BusinessAccount = None):
		"""
		BusinessAccountCustomerUpdateAssigned Constructor.

		:param client: Client
		:param business_account: BusinessAccount
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.assigned = None
		if isinstance(business_account, merchantapi.model.BusinessAccount):
			if business_account.get_id():
				self.set_business_account_id(business_account.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountCustomer_Update_Assigned'

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

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> str:
		"""
		Get Edit_BusinessAccount.

		:returns: str
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_customer_id(self, customer_id: int) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_business_account_id(self, business_account_id: int) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: BusinessAccountCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountCustomerUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		data['Customer_Login'] = self.customer_login
		data['BusinessAccount_Title'] = self.business_account_title
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
