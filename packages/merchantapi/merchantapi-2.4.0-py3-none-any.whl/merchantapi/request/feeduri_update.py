"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request FeedURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feeduri_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class FeedURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		FeedURIUpdate Constructor.

		:param client: Client
		:param uri: Uri
		"""

		super().__init__(client)
		self.uri_id = None
		self.uri = None
		self.status = None
		self.canonical = None
		if isinstance(uri, merchantapi.model.Uri):
			if uri.get_id():
				self.set_uri_id(uri.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURI_Update'

	def get_uri_id(self) -> int:
		"""
		Get URI_ID.

		:returns: int
		"""

		return self.uri_id

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

	def set_uri_id(self, uri_id: int) -> 'FeedURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: FeedURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'FeedURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: FeedURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'FeedURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: FeedURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'FeedURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: FeedURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri_id is not None:
			data['URI_ID'] = self.uri_id

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data
