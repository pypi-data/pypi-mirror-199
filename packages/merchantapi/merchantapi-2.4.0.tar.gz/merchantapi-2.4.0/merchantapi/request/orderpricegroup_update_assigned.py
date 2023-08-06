"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderPriceGroup_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpricegroup_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderPriceGroupUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderPriceGroupUpdateAssigned Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.price_group_id = None
		self.price_group_name = None
		self.assigned = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPriceGroup_Update_Assigned'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_order_id(self, order_id: int) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.order_id = order_id
		return self

	def set_price_group_id(self, price_group_id: int) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderPriceGroupUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPriceGroupUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPriceGroupUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPriceGroupUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
