"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request URI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/uri_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class URIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		URIInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.canonical = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_destination_type(self) -> str:
		"""
		Get Destination_Type.

		:returns: str
		"""

		return self.destination_type

	def get_destination(self) -> str:
		"""
		Get Destination.

		:returns: str
		"""

		return self.destination

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

	def set_uri(self, uri: str) -> 'URIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: URIInsert
		"""

		self.uri = uri
		return self

	def set_destination_type(self, destination_type: str) -> 'URIInsert':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: URIInsert
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'URIInsert':
		"""
		Set Destination.

		:param destination: str
		:returns: URIInsert
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'URIInsert':
		"""
		Set Status.

		:param status: int
		:returns: URIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'URIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: URIInsert
		"""

		self.canonical = canonical
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.uri is not None:
			data['URI'] = self.uri
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data
