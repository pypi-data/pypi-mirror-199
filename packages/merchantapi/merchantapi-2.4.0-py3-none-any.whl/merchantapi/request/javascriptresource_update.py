"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request JavaScriptResource_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/javascriptresource_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class JavaScriptResourceUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, javascript_resource: merchantapi.model.JavaScriptResource = None):
		"""
		JavaScriptResourceUpdate Constructor.

		:param client: Client
		:param javascript_resource: JavaScriptResource
		"""

		super().__init__(client)
		self.javascript_resource_id = None
		self.edit_javascript_resource = None
		self.javascript_resource_code = None
		self.javascript_resource_type = None
		self.javascript_resource_global = None
		self.javascript_resource_active = None
		self.javascript_resource_file_path = None
		self.javascript_resource_attributes = []
		if isinstance(javascript_resource, merchantapi.model.JavaScriptResource):
			if javascript_resource.get_id():
				self.set_javascript_resource_id(javascript_resource.get_id())
			elif javascript_resource.get_code():
				self.set_edit_javascript_resource(javascript_resource.get_code())

			self.set_javascript_resource_code(javascript_resource.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'JavaScriptResource_Update'

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

	def get_javascript_resource_type(self) -> str:
		"""
		Get JavaScriptResource_Type.

		:returns: str
		"""

		return self.javascript_resource_type

	def get_javascript_resource_global(self) -> bool:
		"""
		Get JavaScriptResource_Global.

		:returns: bool
		"""

		return self.javascript_resource_global

	def get_javascript_resource_active(self) -> bool:
		"""
		Get JavaScriptResource_Active.

		:returns: bool
		"""

		return self.javascript_resource_active

	def get_javascript_resource_file_path(self) -> str:
		"""
		Get JavaScriptResource_File_Path.

		:returns: str
		"""

		return self.javascript_resource_file_path

	def get_javascript_resource_attributes(self) -> list:
		"""
		Get JavaScriptResource_Attributes.

		:returns: List of JavaScriptResourceAttribute
		"""

		return self.javascript_resource_attributes

	def set_javascript_resource_id(self, javascript_resource_id: int) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_ID.

		:param javascript_resource_id: int
		:returns: JavaScriptResourceUpdate
		"""

		self.javascript_resource_id = javascript_resource_id
		return self

	def set_edit_javascript_resource(self, edit_javascript_resource: str) -> 'JavaScriptResourceUpdate':
		"""
		Set Edit_JavaScriptResource.

		:param edit_javascript_resource: str
		:returns: JavaScriptResourceUpdate
		"""

		self.edit_javascript_resource = edit_javascript_resource
		return self

	def set_javascript_resource_code(self, javascript_resource_code: str) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_Code.

		:param javascript_resource_code: str
		:returns: JavaScriptResourceUpdate
		"""

		self.javascript_resource_code = javascript_resource_code
		return self

	def set_javascript_resource_type(self, javascript_resource_type: str) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_Type.

		:param javascript_resource_type: str
		:returns: JavaScriptResourceUpdate
		"""

		self.javascript_resource_type = javascript_resource_type
		return self

	def set_javascript_resource_global(self, javascript_resource_global: bool) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_Global.

		:param javascript_resource_global: bool
		:returns: JavaScriptResourceUpdate
		"""

		self.javascript_resource_global = javascript_resource_global
		return self

	def set_javascript_resource_active(self, javascript_resource_active: bool) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_Active.

		:param javascript_resource_active: bool
		:returns: JavaScriptResourceUpdate
		"""

		self.javascript_resource_active = javascript_resource_active
		return self

	def set_javascript_resource_file_path(self, javascript_resource_file_path: str) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_File_Path.

		:param javascript_resource_file_path: str
		:returns: JavaScriptResourceUpdate
		"""

		self.javascript_resource_file_path = javascript_resource_file_path
		return self

	def set_javascript_resource_attributes(self, javascript_resource_attributes: list) -> 'JavaScriptResourceUpdate':
		"""
		Set JavaScriptResource_Attributes.

		:param javascript_resource_attributes: {JavaScriptResourceAttribute[]}
		:raises Exception:
		:returns: JavaScriptResourceUpdate
		"""

		for e in javascript_resource_attributes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceAttribute):
				raise Exception("")
		self.javascript_resource_attributes = javascript_resource_attributes
		return self
	
	def add_javascript_resource_attribute(self, javascript_resource_attribute) -> 'JavaScriptResourceUpdate':
		"""
		Add JavaScriptResource_Attributes.

		:param javascript_resource_attribute: JavaScriptResourceAttribute 
		:raises Exception:
		:returns: {JavaScriptResourceUpdate}
		"""

		if isinstance(javascript_resource_attribute, merchantapi.model.JavaScriptResourceAttribute):
			self.javascript_resource_attributes.append(javascript_resource_attribute)
		elif isinstance(javascript_resource_attribute, dict):
			self.javascript_resource_attributes.append(merchantapi.model.JavaScriptResourceAttribute(javascript_resource_attribute))
		else:
			raise Exception('Expected instance of JavaScriptResourceAttribute or dict')
		return self

	def add_javascript_resource_attributes(self, javascript_resource_attributes: list) -> 'JavaScriptResourceUpdate':
		"""
		Add many JavaScriptResourceAttribute.

		:param javascript_resource_attributes: List of JavaScriptResourceAttribute
		:raises Exception:
		:returns: JavaScriptResourceUpdate
		"""

		for e in javascript_resource_attributes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceAttribute):
				raise Exception('')
			self.javascript_resource_attributes.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.JavaScriptResourceUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'JavaScriptResourceUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.JavaScriptResourceUpdate(self, http_response, data)

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
		data['JavaScriptResource_Type'] = self.javascript_resource_type
		if self.javascript_resource_global is not None:
			data['JavaScriptResource_Global'] = self.javascript_resource_global
		if self.javascript_resource_active is not None:
			data['JavaScriptResource_Active'] = self.javascript_resource_active
		data['JavaScriptResource_File_Path'] = self.javascript_resource_file_path
		if len(self.javascript_resource_attributes):
			data['JavaScriptResource_Attributes'] = []

			for f in self.javascript_resource_attributes:
				data['JavaScriptResource_Attributes'].append(f.to_dict())
		return data
