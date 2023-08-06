"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderItemList_BackOrder. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_backorder
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderItemListBackOrder(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListBackOrder Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		self.date_in_stock = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_BackOrder'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_ids(self):
		"""
		Get Line_IDs.

		:returns: list
		"""

		return self.line_ids

	def get_date_in_stock(self) -> int:
		"""
		Get Date_InStock.

		:returns: int
		"""

		return self.date_in_stock

	def set_order_id(self, order_id: int) -> 'OrderItemListBackOrder':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListBackOrder
		"""

		self.order_id = order_id
		return self

	def set_date_in_stock(self, date_in_stock: int) -> 'OrderItemListBackOrder':
		"""
		Set Date_InStock.

		:param date_in_stock: int
		:returns: OrderItemListBackOrder
		"""

		self.date_in_stock = date_in_stock
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListBackOrder':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListBackOrder}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListBackOrder':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListBackOrder
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListBackOrder':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListBackOrder':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListBackOrder(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		data['Line_IDs'] = self.line_ids
		if self.date_in_stock is not None:
			data['Date_InStock'] = self.date_in_stock
		return data
