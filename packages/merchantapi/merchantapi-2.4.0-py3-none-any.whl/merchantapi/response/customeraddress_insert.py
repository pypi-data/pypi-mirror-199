"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for CustomerAddress_Insert.

:see: https://docs.miva.com/json-api/functions/customeraddress_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class CustomerAddressInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.CustomerAddress(self.data['data'])

	def get_customer_address(self) -> merchantapi.model.CustomerAddress:
		"""
		Get customer_address.

		:returns: CustomerAddress
		"""

		return {} if 'data' not in self.data else self.data['data']
