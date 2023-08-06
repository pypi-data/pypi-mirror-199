"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

RequestBuilder can be used to build out custom request objects to send to the API
"""

import merchantapi.abstract
import merchantapi.listquery
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class RequestBuilder(merchantapi.abstract.Request):
	def __init__(self, client: Client, function: str = '', data: dict = None):
		"""
		RequestBuilder Constructor.

		:param client: Client
		:param function: str
		:param data: dict
		"""
		super().__init__(client)

		if not isinstance(data, dict):
			data = dict()

		self.set_scope(merchantapi.abstract.Request.SCOPE_STORE)
		self.set_function(function)
		self.data = data

	def set_function(self, function: str) -> 'RequestBuilder':
		"""
		Set the request function

		:param function: str
		"""

		self.function = function
		return self

	def get_function(self) -> str:
		"""
		Get the request function

		:param function: str
		"""

		return self.function

	def set_scope(self, scope: int) -> 'RequestBuilder':
		"""
		Set the request scope

		:param scope: int
		"""

		self.scope = scope
		return self

	def set(self, field: str, value) -> 'RequestBuilder':
		"""
		Set a field value

		:param field: str
		:param value: mixed
		"""

		self.data[field] = value
		return self

	def get(self, field: str, default_value=None):
		"""
		Get a field value

		:param field: str
		:param default_value: mixed
		:returns: mixed
		"""

		if field in self.data:
			return self.data[field]
		return default_value

	def has(self, field: str) -> bool:
		"""
		Check if a field exists

		:param field: str
		:returns: bool
		"""

		return field in self.data

	def remove(self, field: str) -> 'RequestBuilder':
		"""
		Remove a field if it exists

		:param field: str
		"""

		if field in self.data:
			self.data.pop(field, None)
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.RequestBuilder':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'merchantapi.response.RequestBuilder':
		"""
		Create a response object from the response data

		:param data:
		:returns: Response
		"""

		return merchantapi.response.RequestBuilder(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""
		ret = super().to_dict()
		ret.update(self.data)

		return ret


"""
ListQueryRequestBuilder can be used to build out custom request objects to send to the API
"""


class ListQueryRequestBuilder(merchantapi.listquery.ListQueryRequest):
	def __init__(self, client: Client, function: str = '', data: dict = None):
		"""
		ListQueryRequestBuilder Constructor.

		:param client: Client
		:param function: str
		:param data: dict
		"""
		
		super().__init__(client)

		if data is None:
			data = {}
		self.set_scope(merchantapi.abstract.Request.SCOPE_STORE)
		self.set_function(function)
		self.data = data

	def set_function(self, function: str) -> 'ListQueryRequestBuilder':
		"""
		Set the request function

		:param function: str
		"""

		self.function = function
		return self

	def get_function(self) -> str:
		"""
		Get the request function

		:param function: str
		"""

		return self.function

	def set_scope(self, scope: int) -> 'ListQueryRequestBuilder':
		"""
		Set the request scope

		:param scope: int
		"""

		self.scope = scope
		return self

	def set(self, field: str, value) -> 'ListQueryRequestBuilder':
		"""
		Set a field value

		:param field: str
		:param value: mixed
		"""

		self.data[field] = value
		return self

	def get(self, field: str, default_value=None):
		"""
		Get a field value

		:param field: str
		:param default_value: mixed
		:returns: mixed
		"""

		if field in self.data:
			return self.data[field]
		return default_value

	def has(self, field: str) -> bool:
		"""
		Check if a field exists

		:param field: str
		:returns: bool
		"""

		return field in self.data

	def remove(self, field: str) -> 'ListQueryRequestBuilder':
		"""
		Remove a field if it exists

		:param field: str
		"""

		if field in self.data:
			self.data.pop(field, None)
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ListQueryRequestBuilder':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'merchantapi.response.ListQueryRequestBuilder':
		"""
		Create a response object from the response data

		:param data:
		:returns: Response
		"""

		return merchantapi.response.ListQueryRequestBuilder(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		ret = super().to_dict()
		ret.update(self.data)

		return ret