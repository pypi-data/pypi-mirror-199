"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderPriceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpricegrouplist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import PriceGroupListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderPriceGroupListLoadQuery(PriceGroupListLoadQuery):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderPriceGroupListLoadQuery Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.assigned = None
		self.unassigned = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPriceGroupList_Load_Query'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_order_id(self, order_id: int) -> 'OrderPriceGroupListLoadQuery':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderPriceGroupListLoadQuery
		"""

		self.order_id = order_id
		return self

	def set_assigned(self, assigned: bool) -> 'OrderPriceGroupListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderPriceGroupListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'OrderPriceGroupListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: OrderPriceGroupListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPriceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPriceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPriceGroupListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
