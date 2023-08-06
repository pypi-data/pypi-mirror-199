"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for CSSResource_Insert.

:see: https://docs.miva.com/json-api/functions/cssresource_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class CSSResourceInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CSSResourceInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.CSSResource(self.data['data'])

	def get_css_resource(self) -> merchantapi.model.CSSResource:
		"""
		Get css_resource.

		:returns: CSSResource
		"""

		return {} if 'data' not in self.data else self.data['data']
