"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for CustomerAddress_Update_Residential.

:see: https://docs.miva.com/json-api/functions/customeraddress_update_residential
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class CustomerAddressUpdateResidential(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerAddressUpdateResidential Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
