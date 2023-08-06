"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for OrderItemList_CreateReturn.

:see: https://docs.miva.com/json-api/functions/orderitemlist_createreturn
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class OrderItemListCreateReturn(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderItemListCreateReturn Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderReturn(self.data['data'])

	def get_order_return(self) -> merchantapi.model.OrderReturn:
		"""
		Get order_return.

		:returns: OrderReturn
		"""

		return {} if 'data' not in self.data else self.data['data']
