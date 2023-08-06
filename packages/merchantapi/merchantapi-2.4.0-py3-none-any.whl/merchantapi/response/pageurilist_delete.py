"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for PageURIList_Delete.

:see: https://docs.miva.com/json-api/functions/pageurilist_delete
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class PageURIListDelete(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PageURIListDelete Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.Uri(e)

	def get_uris(self):
		"""
		Get uris.

		:returns: list of Uri
		"""

		return self.data['data'] if self.data['data'] is not None else []
