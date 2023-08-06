"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BusinessAccountList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccountlist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BusinessAccountListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		BusinessAccountListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.business_account_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccountList_Delete'

	def get_business_account_ids(self):
		"""
		Get BusinessAccount_IDs.

		:returns: list
		"""

		return self.business_account_ids
	
	def add_business_account_id(self, business_account_id) -> 'BusinessAccountListDelete':
		"""
		Add BusinessAccount_IDs.

		:param business_account_id: int
		:returns: {BusinessAccountListDelete}
		"""

		self.business_account_ids.append(business_account_id)
		return self

	def add_business_account(self, business_account: merchantapi.model.BusinessAccount) -> 'BusinessAccountListDelete':
		"""
		Add BusinessAccount model.

		:param business_account: BusinessAccount
		:raises Exception:
		:returns: BusinessAccountListDelete
		"""
		if not isinstance(business_account, merchantapi.model.BusinessAccount):
			raise Exception('Expected an instance of BusinessAccount')

		if business_account.get_id():
			self.business_account_ids.append(business_account.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['BusinessAccount_IDs'] = self.business_account_ids
		return data
