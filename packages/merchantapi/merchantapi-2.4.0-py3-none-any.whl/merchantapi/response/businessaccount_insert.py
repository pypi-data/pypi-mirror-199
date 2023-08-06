"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for BusinessAccount_Insert.

:see: https://docs.miva.com/json-api/functions/businessaccount_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class BusinessAccountInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BusinessAccountInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.BusinessAccount(self.data['data'])

	def get_business_account(self) -> merchantapi.model.BusinessAccount:
		"""
		Get business_account.

		:returns: BusinessAccount
		"""

		return {} if 'data' not in self.data else self.data['data']
