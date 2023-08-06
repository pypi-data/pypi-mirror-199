"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CouponPriceGroup_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponpricegroup_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CouponPriceGroupUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponPriceGroupUpdateAssigned Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.price_group_id = None
		self.price_group_name = None
		self.assigned = None
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())
			elif coupon.get_code():
				self.set_edit_coupon(coupon.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponPriceGroup_Update_Assigned'

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

	def set_coupon_id(self, coupon_id: int) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_price_group_name(self, price_group_name: str) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponPriceGroupUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponPriceGroupUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponPriceGroupUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponPriceGroupUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		data['Assigned'] = self.assigned
		return data
