"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderCoupon_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordercoupon_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderCouponUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCouponUpdateAssigned Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.assigned = None
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderCoupon_Update_Assigned'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_order_id(self, order_id: int) -> 'OrderCouponUpdateAssigned':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCouponUpdateAssigned
		"""

		self.order_id = order_id
		return self

	def set_coupon_id(self, coupon_id: int) -> 'OrderCouponUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: OrderCouponUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'OrderCouponUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: OrderCouponUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'OrderCouponUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: OrderCouponUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_assigned(self, assigned: bool) -> 'OrderCouponUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: OrderCouponUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCouponUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCouponUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCouponUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
