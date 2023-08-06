"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request JavaScriptResource_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/javascriptresource_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class JavaScriptResourceDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, javascript_resource: merchantapi.model.JavaScriptResource = None):
		"""
		JavaScriptResourceDelete Constructor.

		:param client: Client
		:param javascript_resource: JavaScriptResource
		"""

		super().__init__(client)
		self.javascript_resource_id = None
		self.edit_javascript_resource = None
		self.javascript_resource_code = None
		if isinstance(javascript_resource, merchantapi.model.JavaScriptResource):
			if javascript_resource.get_id():
				self.set_javascript_resource_id(javascript_resource.get_id())
			elif javascript_resource.get_code():
				self.set_edit_javascript_resource(javascript_resource.get_code())
			elif javascript_resource.get_code():
				self.set_javascript_resource_code(javascript_resource.get_code())

			self.set_javascript_resource_code(javascript_resource.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'JavaScriptResource_Delete'

	def get_javascript_resource_id(self) -> int:
		"""
		Get JavaScriptResource_ID.

		:returns: int
		"""

		return self.javascript_resource_id

	def get_edit_javascript_resource(self) -> str:
		"""
		Get Edit_JavaScriptResource.

		:returns: str
		"""

		return self.edit_javascript_resource

	def get_javascript_resource_code(self) -> str:
		"""
		Get JavaScriptResource_Code.

		:returns: str
		"""

		return self.javascript_resource_code

	def set_javascript_resource_id(self, javascript_resource_id: int) -> 'JavaScriptResourceDelete':
		"""
		Set JavaScriptResource_ID.

		:param javascript_resource_id: int
		:returns: JavaScriptResourceDelete
		"""

		self.javascript_resource_id = javascript_resource_id
		return self

	def set_edit_javascript_resource(self, edit_javascript_resource: str) -> 'JavaScriptResourceDelete':
		"""
		Set Edit_JavaScriptResource.

		:param edit_javascript_resource: str
		:returns: JavaScriptResourceDelete
		"""

		self.edit_javascript_resource = edit_javascript_resource
		return self

	def set_javascript_resource_code(self, javascript_resource_code: str) -> 'JavaScriptResourceDelete':
		"""
		Set JavaScriptResource_Code.

		:param javascript_resource_code: str
		:returns: JavaScriptResourceDelete
		"""

		self.javascript_resource_code = javascript_resource_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.JavaScriptResourceDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'JavaScriptResourceDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.JavaScriptResourceDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.javascript_resource_id is not None:
			data['JavaScriptResource_ID'] = self.javascript_resource_id
		elif self.edit_javascript_resource is not None:
			data['Edit_JavaScriptResource'] = self.edit_javascript_resource
		elif self.javascript_resource_code is not None:
			data['JavaScriptResource_Code'] = self.javascript_resource_code

		if self.javascript_resource_code is not None:
			data['JavaScriptResource_Code'] = self.javascript_resource_code
		return data
