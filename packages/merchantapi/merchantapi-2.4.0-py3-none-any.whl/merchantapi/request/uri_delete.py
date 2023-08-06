"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request URI_Delete. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/uri_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class URIDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		URIDelete Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.uri_id = None
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URI_Delete'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def set_uri_id(self, uri_id: int) -> 'URIDelete':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: URIDelete
		"""

		self.uri_id = uri_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		return data
