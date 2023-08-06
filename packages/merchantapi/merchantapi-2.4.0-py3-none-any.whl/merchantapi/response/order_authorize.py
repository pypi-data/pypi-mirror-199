"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for Order_Authorize.

:see: https://docs.miva.com/json-api/functions/order_authorize
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class OrderAuthorize(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OrderAuthorize Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.OrderPaymentAuthorize(self.data['data'])

	def get_order_payment_authorize(self) -> merchantapi.model.OrderPaymentAuthorize:
		"""
		Get order_payment_authorize.

		:returns: OrderPaymentAuthorize
		"""

		return {} if 'data' not in self.data else self.data['data']
