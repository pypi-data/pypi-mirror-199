"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request FeedURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feeduri_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class FeedURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		FeedURIInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.feed_id = None
		self.feed_code = None
		self.uri = None
		self.status = None
		self.canonical = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURI_Insert'

	def get_feed_id(self) -> int:
		"""
		Get Feed_ID.

		:returns: int
		"""

		return self.feed_id

	def get_feed_code(self) -> str:
		"""
		Get Feed_Code.

		:returns: str
		"""

		return self.feed_code

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

	def set_feed_id(self, feed_id: int) -> 'FeedURIInsert':
		"""
		Set Feed_ID.

		:param feed_id: int
		:returns: FeedURIInsert
		"""

		self.feed_id = feed_id
		return self

	def set_feed_code(self, feed_code: str) -> 'FeedURIInsert':
		"""
		Set Feed_Code.

		:param feed_code: str
		:returns: FeedURIInsert
		"""

		self.feed_code = feed_code
		return self

	def set_uri(self, uri: str) -> 'FeedURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: FeedURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'FeedURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: FeedURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'FeedURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: FeedURIInsert
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.feed_id is not None:
			data['Feed_ID'] = self.feed_id
		elif self.feed_code is not None:
			data['Feed_Code'] = self.feed_code

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data
