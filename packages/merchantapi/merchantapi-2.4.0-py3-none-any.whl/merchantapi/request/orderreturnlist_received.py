"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderReturnList_Received. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderreturnlist_received
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderReturnListReceived(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OrderReturnListReceived Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.returns = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderReturnList_Received'

	def get_returns(self) -> list:
		"""
		Get Returns.

		:returns: List of ReceivedReturn
		"""

		return self.returns

	def set_returns(self, returns: list) -> 'OrderReturnListReceived':
		"""
		Set Returns.

		:param returns: {ReceivedReturn[]}
		:raises Exception:
		:returns: OrderReturnListReceived
		"""

		for e in returns:
			if not isinstance(e, merchantapi.model.ReceivedReturn):
				raise Exception("")
		self.returns = returns
		return self
	
	def add_received_return(self, received_return) -> 'OrderReturnListReceived':
		"""
		Add Returns.

		:param received_return: ReceivedReturn 
		:raises Exception:
		:returns: {OrderReturnListReceived}
		"""

		if isinstance(received_return, merchantapi.model.ReceivedReturn):
			self.returns.append(received_return)
		elif isinstance(received_return, dict):
			self.returns.append(merchantapi.model.ReceivedReturn(received_return))
		else:
			raise Exception('Expected instance of ReceivedReturn or dict')
		return self

	def add_returns(self, returns: list) -> 'OrderReturnListReceived':
		"""
		Add many ReceivedReturn.

		:param returns: List of ReceivedReturn
		:raises Exception:
		:returns: OrderReturnListReceived
		"""

		for e in returns:
			if not isinstance(e, merchantapi.model.ReceivedReturn):
				raise Exception('')
			self.returns.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderReturnListReceived':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderReturnListReceived':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderReturnListReceived(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if len(self.returns):
			data['Returns'] = []

			for f in self.returns:
				data['Returns'].append(f.to_dict())
		return data
