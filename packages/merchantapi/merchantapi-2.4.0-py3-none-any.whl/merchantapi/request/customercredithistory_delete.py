"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerCreditHistory_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customercredithistory_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerCreditHistoryDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer_credit_history: merchantapi.model.CustomerCreditHistory = None):
		"""
		CustomerCreditHistoryDelete Constructor.

		:param client: Client
		:param customer_credit_history: CustomerCreditHistory
		"""

		super().__init__(client)
		self.customer_credit_history_id = None
		if isinstance(customer_credit_history, merchantapi.model.CustomerCreditHistory):
			self.set_customer_credit_history_id(customer_credit_history.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerCreditHistory_Delete'

	def get_customer_credit_history_id(self) -> int:
		"""
		Get CustomerCreditHistory_ID.

		:returns: int
		"""

		return self.customer_credit_history_id

	def set_customer_credit_history_id(self, customer_credit_history_id: int) -> 'CustomerCreditHistoryDelete':
		"""
		Set CustomerCreditHistory_ID.

		:param customer_credit_history_id: int
		:returns: CustomerCreditHistoryDelete
		"""

		self.customer_credit_history_id = customer_credit_history_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerCreditHistoryDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerCreditHistoryDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerCreditHistoryDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['CustomerCreditHistory_ID'] = self.customer_credit_history_id
		return data
