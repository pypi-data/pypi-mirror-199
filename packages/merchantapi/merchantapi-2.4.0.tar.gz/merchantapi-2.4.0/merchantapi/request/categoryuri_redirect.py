"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryURI_Redirect. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryuri_redirect
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryURIRedirect(ListQueryRequest):
	def __init__(self, client: Client = None):
		"""
		CategoryURIRedirect Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.destination_store_code = None
		self.destination_type = None
		self.destination = None
		self.status = None
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURI_Redirect'

	def get_destination_store_code(self) -> str:
		"""
		Get Destination_Store_Code.

		:returns: str
		"""

		return self.destination_store_code

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

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids

	def set_destination_store_code(self, destination_store_code: str) -> 'CategoryURIRedirect':
		"""
		Set Destination_Store_Code.

		:param destination_store_code: str
		:returns: CategoryURIRedirect
		"""

		self.destination_store_code = destination_store_code
		return self

	def set_destination_type(self, destination_type: str) -> 'CategoryURIRedirect':
		"""
		Set Destination_Type.

		:param destination_type: str
		:returns: CategoryURIRedirect
		"""

		self.destination_type = destination_type
		return self

	def set_destination(self, destination: str) -> 'CategoryURIRedirect':
		"""
		Set Destination.

		:param destination: str
		:returns: CategoryURIRedirect
		"""

		self.destination = destination
		return self

	def set_status(self, status: int) -> 'CategoryURIRedirect':
		"""
		Set Status.

		:param status: int
		:returns: CategoryURIRedirect
		"""

		self.status = status
		return self
	
	def add_uri_id(self, uri_id) -> 'CategoryURIRedirect':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {CategoryURIRedirect}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'CategoryURIRedirect':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: CategoryURIRedirect
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIRedirect':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIRedirect':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIRedirect(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.destination_store_code is not None:
			data['Destination_Store_Code'] = self.destination_store_code
		if self.destination_type is not None:
			data['Destination_Type'] = self.destination_type
		if self.destination is not None:
			data['Destination'] = self.destination
		if self.status is not None:
			data['Status'] = self.status
		data['URI_IDs'] = self.uri_ids
		return data
