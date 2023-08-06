"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductURIList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturilist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductURIListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProductURIListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.uri_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURIList_Delete'

	def get_uri_ids(self):
		"""
		Get URI_IDs.

		:returns: list
		"""

		return self.uri_ids
	
	def add_uri_id(self, uri_id) -> 'ProductURIListDelete':
		"""
		Add URI_IDs.

		:param uri_id: int
		:returns: {ProductURIListDelete}
		"""

		self.uri_ids.append(uri_id)
		return self

	def add_uri(self, uri: merchantapi.model.Uri) -> 'ProductURIListDelete':
		"""
		Add Uri model.

		:param uri: Uri
		:raises Exception:
		:returns: ProductURIListDelete
		"""
		if not isinstance(uri, merchantapi.model.Uri):
			raise Exception('Expected an instance of Uri')

		if uri.get_id():
			self.uri_ids.append(uri.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['URI_IDs'] = self.uri_ids
		return data
