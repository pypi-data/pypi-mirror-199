"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderItem_Split. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitem_split
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderItemSplit(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_item: merchantapi.model.OrderItem = None):
		"""
		OrderItemSplit Constructor.

		:param client: Client
		:param order_item: OrderItem
		"""

		super().__init__(client)
		self.order_id = None
		self.line_id = None
		self.quantity = None
		if isinstance(order_item, merchantapi.model.OrderItem):
			if order_item.get_order_id():
				self.set_order_id(order_item.get_order_id())

			if order_item.get_line_id():
				self.set_line_id(order_item.get_line_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItem_Split'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_id(self) -> int:
		"""
		Get Line_ID.

		:returns: int
		"""

		return self.line_id

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def set_order_id(self, order_id: int) -> 'OrderItemSplit':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemSplit
		"""

		self.order_id = order_id
		return self

	def set_line_id(self, line_id: int) -> 'OrderItemSplit':
		"""
		Set Line_ID.

		:param line_id: int
		:returns: OrderItemSplit
		"""

		self.line_id = line_id
		return self

	def set_quantity(self, quantity: int) -> 'OrderItemSplit':
		"""
		Set Quantity.

		:param quantity: int
		:returns: OrderItemSplit
		"""

		self.quantity = quantity
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemSplit':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemSplit':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemSplit(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.line_id is not None:
			data['Line_ID'] = self.line_id

		data['Quantity'] = self.quantity
		return data
