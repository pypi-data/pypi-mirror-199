"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request URIList_Delete. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/urilist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class URIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		URIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'URIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {URIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'URIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: URIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data
