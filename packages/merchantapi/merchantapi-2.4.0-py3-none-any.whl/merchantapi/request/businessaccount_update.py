"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BusinessAccount_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccount_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BusinessAccountUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, business_account: merchantapi.model.BusinessAccount = None):
		"""
		BusinessAccountUpdate Constructor.

		:param client: Client
		:param business_account: BusinessAccount
		"""

		super().__init__(client)
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.business_account_tax_exempt = None
		if isinstance(business_account, merchantapi.model.BusinessAccount):
			if business_account.get_id():
				self.set_business_account_id(business_account.get_id())

			self.set_business_account_title(business_account.get_title())
			self.set_business_account_tax_exempt(business_account.get_tax_exempt())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccount_Update'

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

	def get_business_account_tax_exempt(self) -> bool:
		"""
		Get BusinessAccount_Tax_Exempt.

		:returns: bool
		"""

		return self.business_account_tax_exempt

	def set_business_account_id(self, business_account_id: int) -> 'BusinessAccountUpdate':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: BusinessAccountUpdate
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: int) -> 'BusinessAccountUpdate':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: int
		:returns: BusinessAccountUpdate
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountUpdate':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountUpdate
		"""

		self.business_account_title = business_account_title
		return self

	def set_business_account_tax_exempt(self, business_account_tax_exempt: bool) -> 'BusinessAccountUpdate':
		"""
		Set BusinessAccount_Tax_Exempt.

		:param business_account_tax_exempt: bool
		:returns: BusinessAccountUpdate
		"""

		self.business_account_tax_exempt = business_account_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountUpdate(self, http_response, data)

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

		if self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title
		if self.business_account_tax_exempt is not None:
			data['BusinessAccount_Tax_Exempt'] = self.business_account_tax_exempt
		return data
