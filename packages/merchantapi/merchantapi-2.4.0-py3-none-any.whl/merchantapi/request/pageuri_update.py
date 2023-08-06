"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PageURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageuri_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		PageURIUpdate Constructor.

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

		return 'PageURI_Update'

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

	def set_uri_id(self, uri_id: int) -> 'PageURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: PageURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'PageURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: PageURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'PageURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: PageURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'PageURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: PageURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIUpdate(self, http_response, data)

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
