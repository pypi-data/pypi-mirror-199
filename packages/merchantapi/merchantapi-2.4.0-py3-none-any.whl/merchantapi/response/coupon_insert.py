"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for Coupon_Insert.

:see: https://docs.miva.com/json-api/functions/coupon_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class CouponInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CouponInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.Coupon(self.data['data'])

	def get_coupon(self) -> merchantapi.model.Coupon:
		"""
		Get coupon.

		:returns: Coupon
		"""

		return {} if 'data' not in self.data else self.data['data']
