"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryURI_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryuri_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryURIUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, uri: merchantapi.model.Uri = None):
		"""
		CategoryURIUpdate Constructor.

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

		return 'CategoryURI_Update'

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

	def set_uri_id(self, uri_id: int) -> 'CategoryURIUpdate':
		"""
		Set URI_ID.

		:param uri_id: int
		:returns: CategoryURIUpdate
		"""

		self.uri_id = uri_id
		return self

	def set_uri(self, uri: str) -> 'CategoryURIUpdate':
		"""
		Set URI.

		:param uri: str
		:returns: CategoryURIUpdate
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'CategoryURIUpdate':
		"""
		Set Status.

		:param status: int
		:returns: CategoryURIUpdate
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'CategoryURIUpdate':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: CategoryURIUpdate
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIUpdate(self, http_response, data)

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
