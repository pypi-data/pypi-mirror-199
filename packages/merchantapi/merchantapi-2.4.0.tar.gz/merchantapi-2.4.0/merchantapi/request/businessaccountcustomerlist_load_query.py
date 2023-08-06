"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BusinessAccountCustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountcustomerlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import CustomerListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BusinessAccountCustomerListLoadQuery(CustomerListLoadQuery):
	def __init__(self, client: Client = None):
		"""
		BusinessAccountCustomerListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.assigned = None
		self.unassigned = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountCustomerList_Load_Query'

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> int:
		"""
		Get Edit_BusinessAccount.

		:returns: int
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

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_business_account_id(self, business_account_id: int) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: int) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: int
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: BusinessAccountCustomerListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountCustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountCustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountCustomerListLoadQuery(self, http_response, data)

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

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
