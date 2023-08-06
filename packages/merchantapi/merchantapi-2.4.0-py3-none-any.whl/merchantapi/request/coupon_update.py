"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Coupon_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/coupon_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CouponUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponUpdate Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.coupon_code = None
		self.edit_coupon = None
		self.code = None
		self.description = None
		self.customer_scope = None
		self.date_time_start = None
		self.date_time_end = None
		self.max_use = None
		self.max_per = None
		self.active = None
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())
			elif coupon.get_code():
				self.set_edit_coupon(coupon.get_code())

			self.set_coupon_code(coupon.get_code())
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

		return 'Coupon_Update'

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

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

	def set_coupon_id(self, coupon_id: int) -> 'CouponUpdate':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponUpdate
		"""

		self.coupon_id = coupon_id
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponUpdate':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponUpdate
		"""

		self.coupon_code = coupon_code
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponUpdate':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponUpdate
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_code(self, code: str) -> 'CouponUpdate':
		"""
		Set Code.

		:param code: str
		:returns: CouponUpdate
		"""

		self.code = code
		return self

	def set_description(self, description: str) -> 'CouponUpdate':
		"""
		Set Description.

		:param description: str
		:returns: CouponUpdate
		"""

		self.description = description
		return self

	def set_customer_scope(self, customer_scope: str) -> 'CouponUpdate':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: CouponUpdate
		"""

		self.customer_scope = customer_scope
		return self

	def set_date_time_start(self, date_time_start: int) -> 'CouponUpdate':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: CouponUpdate
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'CouponUpdate':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: CouponUpdate
		"""

		self.date_time_end = date_time_end
		return self

	def set_max_use(self, max_use: int) -> 'CouponUpdate':
		"""
		Set Max_Use.

		:param max_use: int
		:returns: CouponUpdate
		"""

		self.max_use = max_use
		return self

	def set_max_per(self, max_per: int) -> 'CouponUpdate':
		"""
		Set Max_Per.

		:param max_per: int
		:returns: CouponUpdate
		"""

		self.max_per = max_per
		return self

	def set_active(self, active: bool) -> 'CouponUpdate':
		"""
		Set Active.

		:param active: bool
		:returns: CouponUpdate
		"""

		self.active = active
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponUpdate(self, http_response, data)

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

		if self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code
		if self.code is not None:
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
		return data
