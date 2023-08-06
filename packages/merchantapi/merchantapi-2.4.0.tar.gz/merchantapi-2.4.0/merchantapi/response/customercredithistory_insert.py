"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for CustomerCreditHistory_Insert.

:see: https://docs.miva.com/json-api/functions/customercredithistory_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class CustomerCreditHistoryInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerCreditHistoryInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.CustomerCreditHistory(self.data['data'])

	def get_customer_credit_history(self) -> merchantapi.model.CustomerCreditHistory:
		"""
		Get customer_credit_history.

		:returns: CustomerCreditHistory
		"""

		return {} if 'data' not in self.data else self.data['data']
