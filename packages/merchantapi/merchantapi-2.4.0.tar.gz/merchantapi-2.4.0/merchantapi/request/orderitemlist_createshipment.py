"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderItemList_CreateShipment. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitemlist_createshipment
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderItemListCreateShipment(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemListCreateShipment Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.line_ids = []
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItemList_CreateShipment'

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

	def set_order_id(self, order_id: int) -> 'OrderItemListCreateShipment':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemListCreateShipment
		"""

		self.order_id = order_id
		return self
	
	def add_line_id(self, line_id) -> 'OrderItemListCreateShipment':
		"""
		Add Line_IDs.

		:param line_id: int
		:returns: {OrderItemListCreateShipment}
		"""

		self.line_ids.append(line_id)
		return self

	def add_order_item(self, order_item: merchantapi.model.OrderItem) -> 'OrderItemListCreateShipment':
		"""
		Add OrderItem model.

		:param order_item: OrderItem
		:raises Exception:
		:returns: OrderItemListCreateShipment
		"""
		if not isinstance(order_item, merchantapi.model.OrderItem):
			raise Exception('Expected an instance of OrderItem')

		if order_item.get_line_id():
			self.line_ids.append(order_item.get_line_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemListCreateShipment':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemListCreateShipment':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemListCreateShipment(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Line_IDs'] = self.line_ids
		return data
