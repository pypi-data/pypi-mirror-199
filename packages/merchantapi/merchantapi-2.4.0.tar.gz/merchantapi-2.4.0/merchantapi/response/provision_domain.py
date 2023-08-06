"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for Provision_Domain.

:see: https://docs.miva.com/json-api/functions/provision_domain
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class ProvisionDomain(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProvisionDomain Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.ProvisionMessage(e)

	def get_provision_messages(self):
		"""
		Get provision_messages.

		:returns: list of ProvisionMessage
		"""

		return self.data['data'] if self.data['data'] is not None else []
