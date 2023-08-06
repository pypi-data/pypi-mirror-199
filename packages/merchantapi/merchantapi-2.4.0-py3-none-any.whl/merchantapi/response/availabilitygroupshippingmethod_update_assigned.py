"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for AvailabilityGroupShippingMethod_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/availabilitygroupshippingmethod_update_assigned
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class AvailabilityGroupShippingMethodUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AvailabilityGroupShippingMethodUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
