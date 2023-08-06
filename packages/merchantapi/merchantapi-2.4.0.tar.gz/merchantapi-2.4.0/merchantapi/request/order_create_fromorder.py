"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Order_Create_FromOrder. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_create_fromorder
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderCreateFromOrder(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCreateFromOrder Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Create_FromOrder'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def set_order_id(self, order_id: int) -> 'OrderCreateFromOrder':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCreateFromOrder
		"""

		self.order_id = order_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCreateFromOrder':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCreateFromOrder':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCreateFromOrder(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		return data
