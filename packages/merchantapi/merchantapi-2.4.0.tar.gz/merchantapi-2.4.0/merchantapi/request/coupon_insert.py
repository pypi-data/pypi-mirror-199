"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Coupon_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/coupon_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CouponInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponInsert Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.code = None
		self.description = None
		self.customer_scope = None
		self.date_time_start = None
		self.date_time_end = None
		self.max_use = None
		self.max_per = None
		self.active = None
		self.price_group_id = None
		if isinstance(coupon, merchantapi.model.Coupon):
			self.set_code(coupon.get_code())
			self.set_description(coupon.get_description())
			self.set_customer_scope(coupon.get_customer_scope())
			self.set_date_time_start(coupon.get_date_time_start())
			self.set_date_time_end(coupon.get_date_time_end())
			self.set_max_use(coupon.get_max_use())
			self.set_max_per(coupon.get_max_per())
			self.set_active(coupon.get_active())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Coupon_Insert'

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_customer_scope(self) -> str:
		"""
		Get CustomerScope.

		:returns: str
		"""

		return self.customer_scope

	def get_date_time_start(self) -> int:
		"""
		Get DateTime_Start.

		:returns: int
		"""

		return self.date_time_start

	def get_date_time_end(self) -> int:
		"""
		Get DateTime_End.

		:returns: int
		"""

		return self.date_time_end

	def get_max_use(self) -> int:
		"""
		Get Max_Use.

		:returns: int
		"""

		return self.max_use

	def get_max_per(self) -> int:
		"""
		Get Max_Per.

		:returns: int
		"""

		return self.max_per

	def get_active(self) -> bool:
		"""
		Get Active.

		:returns: bool
		"""

		return self.active

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def set_code(self, code: str) -> 'CouponInsert':
		"""
		Set Code.

		:param code: str
		:returns: CouponInsert
		"""

		self.code = code
		return self

	def set_description(self, description: str) -> 'CouponInsert':
		"""
		Set Description.

		:param description: str
		:returns: CouponInsert
		"""

		self.description = description
		return self

	def set_customer_scope(self, customer_scope: str) -> 'CouponInsert':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: CouponInsert
		"""

		self.customer_scope = customer_scope
		return self

	def set_date_time_start(self, date_time_start: int) -> 'CouponInsert':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: CouponInsert
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'CouponInsert':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: CouponInsert
		"""

		self.date_time_end = date_time_end
		return self

	def set_max_use(self, max_use: int) -> 'CouponInsert':
		"""
		Set Max_Use.

		:param max_use: int
		:returns: CouponInsert
		"""

		self.max_use = max_use
		return self

	def set_max_per(self, max_per: int) -> 'CouponInsert':
		"""
		Set Max_Per.

		:param max_per: int
		:returns: CouponInsert
		"""

		self.max_per = max_per
		return self

	def set_active(self, active: bool) -> 'CouponInsert':
		"""
		Set Active.

		:param active: bool
		:returns: CouponInsert
		"""

		self.active = active
		return self

	def set_price_group_id(self, price_group_id: int) -> 'CouponInsert':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: CouponInsert
		"""

		self.price_group_id = price_group_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Code'] = self.code
		if self.description is not None:
			data['Description'] = self.description
		if self.customer_scope is not None:
			data['CustomerScope'] = self.customer_scope
		if self.date_time_start is not None:
			data['DateTime_Start'] = self.date_time_start
		if self.date_time_end is not None:
			data['DateTime_End'] = self.date_time_end
		if self.max_use is not None:
			data['Max_Use'] = self.max_use
		if self.max_per is not None:
			data['Max_Per'] = self.max_per
		if self.active is not None:
			data['Active'] = self.active
		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		return data
