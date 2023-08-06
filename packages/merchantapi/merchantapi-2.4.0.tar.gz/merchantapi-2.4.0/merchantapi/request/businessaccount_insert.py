"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BusinessAccount_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/businessaccount_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BusinessAccountInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		BusinessAccountInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.business_account_title = None
		self.business_account_tax_exempt = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BusinessAccount_Insert'

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

	def set_business_account_title(self, business_account_title: str) -> 'BusinessAccountInsert':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: BusinessAccountInsert
		"""

		self.business_account_title = business_account_title
		return self

	def set_business_account_tax_exempt(self, business_account_tax_exempt: bool) -> 'BusinessAccountInsert':
		"""
		Set BusinessAccount_Tax_Exempt.

		:param business_account_tax_exempt: bool
		:returns: BusinessAccountInsert
		"""

		self.business_account_tax_exempt = business_account_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BusinessAccountInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BusinessAccountInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BusinessAccountInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title
		if self.business_account_tax_exempt is not None:
			data['BusinessAccount_Tax_Exempt'] = self.business_account_tax_exempt
		return data
