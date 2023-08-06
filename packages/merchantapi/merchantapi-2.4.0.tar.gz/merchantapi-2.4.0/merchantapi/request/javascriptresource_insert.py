"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request JavaScriptResource_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/javascriptresource_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class JavaScriptResourceInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		JavaScriptResourceInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.javascript_resource_code = None
		self.javascript_resource_type = None
		self.javascript_resource_global = None
		self.javascript_resource_active = None
		self.javascript_resource_file_path = None
		self.javascript_resource_attributes = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'JavaScriptResource_Insert'

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

	def set_javascript_resource_code(self, javascript_resource_code: str) -> 'JavaScriptResourceInsert':
		"""
		Set JavaScriptResource_Code.

		:param javascript_resource_code: str
		:returns: JavaScriptResourceInsert
		"""

		self.javascript_resource_code = javascript_resource_code
		return self

	def set_javascript_resource_type(self, javascript_resource_type: str) -> 'JavaScriptResourceInsert':
		"""
		Set JavaScriptResource_Type.

		:param javascript_resource_type: str
		:returns: JavaScriptResourceInsert
		"""

		self.javascript_resource_type = javascript_resource_type
		return self

	def set_javascript_resource_global(self, javascript_resource_global: bool) -> 'JavaScriptResourceInsert':
		"""
		Set JavaScriptResource_Global.

		:param javascript_resource_global: bool
		:returns: JavaScriptResourceInsert
		"""

		self.javascript_resource_global = javascript_resource_global
		return self

	def set_javascript_resource_active(self, javascript_resource_active: bool) -> 'JavaScriptResourceInsert':
		"""
		Set JavaScriptResource_Active.

		:param javascript_resource_active: bool
		:returns: JavaScriptResourceInsert
		"""

		self.javascript_resource_active = javascript_resource_active
		return self

	def set_javascript_resource_file_path(self, javascript_resource_file_path: str) -> 'JavaScriptResourceInsert':
		"""
		Set JavaScriptResource_File_Path.

		:param javascript_resource_file_path: str
		:returns: JavaScriptResourceInsert
		"""

		self.javascript_resource_file_path = javascript_resource_file_path
		return self

	def set_javascript_resource_attributes(self, javascript_resource_attributes: list) -> 'JavaScriptResourceInsert':
		"""
		Set JavaScriptResource_Attributes.

		:param javascript_resource_attributes: {JavaScriptResourceAttribute[]}
		:raises Exception:
		:returns: JavaScriptResourceInsert
		"""

		for e in javascript_resource_attributes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceAttribute):
				raise Exception("")
		self.javascript_resource_attributes = javascript_resource_attributes
		return self
	
	def add_javascript_resource_attribute(self, javascript_resource_attribute) -> 'JavaScriptResourceInsert':
		"""
		Add JavaScriptResource_Attributes.

		:param javascript_resource_attribute: JavaScriptResourceAttribute 
		:raises Exception:
		:returns: {JavaScriptResourceInsert}
		"""

		if isinstance(javascript_resource_attribute, merchantapi.model.JavaScriptResourceAttribute):
			self.javascript_resource_attributes.append(javascript_resource_attribute)
		elif isinstance(javascript_resource_attribute, dict):
			self.javascript_resource_attributes.append(merchantapi.model.JavaScriptResourceAttribute(javascript_resource_attribute))
		else:
			raise Exception('Expected instance of JavaScriptResourceAttribute or dict')
		return self

	def add_javascript_resource_attributes(self, javascript_resource_attributes: list) -> 'JavaScriptResourceInsert':
		"""
		Add many JavaScriptResourceAttribute.

		:param javascript_resource_attributes: List of JavaScriptResourceAttribute
		:raises Exception:
		:returns: JavaScriptResourceInsert
		"""

		for e in javascript_resource_attributes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceAttribute):
				raise Exception('')
			self.javascript_resource_attributes.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.JavaScriptResourceInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'JavaScriptResourceInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.JavaScriptResourceInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

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
