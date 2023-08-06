"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CouponList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponlist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CouponListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CouponListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.coupon_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponList_Delete'

	def get_coupon_ids(self):
		"""
		Get Coupon_IDs.

		:returns: list
		"""

		return self.coupon_ids
	
	def add_coupon_id(self, coupon_id) -> 'CouponListDelete':
		"""
		Add Coupon_IDs.

		:param coupon_id: int
		:returns: {CouponListDelete}
		"""

		self.coupon_ids.append(coupon_id)
		return self

	def add_coupon(self, coupon: merchantapi.model.Coupon) -> 'CouponListDelete':
		"""
		Add Coupon model.

		:param coupon: Coupon
		:raises Exception:
		:returns: CouponListDelete
		"""
		if not isinstance(coupon, merchantapi.model.Coupon):
			raise Exception('Expected an instance of Coupon')

		if coupon.get_id():
			self.coupon_ids.append(coupon.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Coupon_IDs'] = self.coupon_ids
		return data
