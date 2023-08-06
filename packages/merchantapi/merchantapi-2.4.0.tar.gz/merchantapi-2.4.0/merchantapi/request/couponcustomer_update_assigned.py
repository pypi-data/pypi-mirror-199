"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CouponCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponcustomer_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CouponCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponCustomerUpdateAssigned Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.assigned = None
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())

			self.set_coupon_code(coupon.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponCustomer_Update_Assigned'

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

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

	def set_customer_id(self, customer_id: int) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CouponCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_coupon_id(self, coupon_id: int) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponCustomerUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponCustomerUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_assigned(self, assigned: bool) -> 'CouponCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponCustomerUpdateAssigned(self, http_response, data)

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

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		data['Customer_Login'] = self.customer_login
		data['Coupon_Code'] = self.coupon_code
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
