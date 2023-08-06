"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CSSResource_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/cssresource_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CSSResourceUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, css_resource: merchantapi.model.CSSResource = None):
		"""
		CSSResourceUpdate Constructor.

		:param client: Client
		:param css_resource: CSSResource
		"""

		super().__init__(client)
		self.css_resource_id = None
		self.edit_css_resource = None
		self.css_resource_code = None
		self.css_resource_global = None
		self.css_resource_active = None
		self.css_resource_file_path = None
		self.css_resource_attributes = []
		if isinstance(css_resource, merchantapi.model.CSSResource):
			if css_resource.get_id():
				self.set_css_resource_id(css_resource.get_id())
			elif css_resource.get_code():
				self.set_edit_css_resource(css_resource.get_code())

			self.set_css_resource_code(css_resource.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CSSResource_Update'

	def get_css_resource_id(self) -> int:
		"""
		Get CSSResource_ID.

		:returns: int
		"""

		return self.css_resource_id

	def get_edit_css_resource(self) -> str:
		"""
		Get Edit_CSSResource.

		:returns: str
		"""

		return self.edit_css_resource

	def get_css_resource_code(self) -> str:
		"""
		Get CSSResource_Code.

		:returns: str
		"""

		return self.css_resource_code

	def get_css_resource_global(self) -> bool:
		"""
		Get CSSResource_Global.

		:returns: bool
		"""

		return self.css_resource_global

	def get_css_resource_active(self) -> bool:
		"""
		Get CSSResource_Active.

		:returns: bool
		"""

		return self.css_resource_active

	def get_css_resource_file_path(self) -> str:
		"""
		Get CSSResource_File_Path.

		:returns: str
		"""

		return self.css_resource_file_path

	def get_css_resource_attributes(self) -> list:
		"""
		Get CSSResource_Attributes.

		:returns: List of CSSResourceAttribute
		"""

		return self.css_resource_attributes

	def set_css_resource_id(self, css_resource_id: int) -> 'CSSResourceUpdate':
		"""
		Set CSSResource_ID.

		:param css_resource_id: int
		:returns: CSSResourceUpdate
		"""

		self.css_resource_id = css_resource_id
		return self

	def set_edit_css_resource(self, edit_css_resource: str) -> 'CSSResourceUpdate':
		"""
		Set Edit_CSSResource.

		:param edit_css_resource: str
		:returns: CSSResourceUpdate
		"""

		self.edit_css_resource = edit_css_resource
		return self

	def set_css_resource_code(self, css_resource_code: str) -> 'CSSResourceUpdate':
		"""
		Set CSSResource_Code.

		:param css_resource_code: str
		:returns: CSSResourceUpdate
		"""

		self.css_resource_code = css_resource_code
		return self

	def set_css_resource_global(self, css_resource_global: bool) -> 'CSSResourceUpdate':
		"""
		Set CSSResource_Global.

		:param css_resource_global: bool
		:returns: CSSResourceUpdate
		"""

		self.css_resource_global = css_resource_global
		return self

	def set_css_resource_active(self, css_resource_active: bool) -> 'CSSResourceUpdate':
		"""
		Set CSSResource_Active.

		:param css_resource_active: bool
		:returns: CSSResourceUpdate
		"""

		self.css_resource_active = css_resource_active
		return self

	def set_css_resource_file_path(self, css_resource_file_path: str) -> 'CSSResourceUpdate':
		"""
		Set CSSResource_File_Path.

		:param css_resource_file_path: str
		:returns: CSSResourceUpdate
		"""

		self.css_resource_file_path = css_resource_file_path
		return self

	def set_css_resource_attributes(self, css_resource_attributes: list) -> 'CSSResourceUpdate':
		"""
		Set CSSResource_Attributes.

		:param css_resource_attributes: {CSSResourceAttribute[]}
		:raises Exception:
		:returns: CSSResourceUpdate
		"""

		for e in css_resource_attributes:
			if not isinstance(e, merchantapi.model.CSSResourceAttribute):
				raise Exception("")
		self.css_resource_attributes = css_resource_attributes
		return self
	
	def add_css_resource_attribute(self, css_resource_attribute) -> 'CSSResourceUpdate':
		"""
		Add CSSResource_Attributes.

		:param css_resource_attribute: CSSResourceAttribute 
		:raises Exception:
		:returns: {CSSResourceUpdate}
		"""

		if isinstance(css_resource_attribute, merchantapi.model.CSSResourceAttribute):
			self.css_resource_attributes.append(css_resource_attribute)
		elif isinstance(css_resource_attribute, dict):
			self.css_resource_attributes.append(merchantapi.model.CSSResourceAttribute(css_resource_attribute))
		else:
			raise Exception('Expected instance of CSSResourceAttribute or dict')
		return self

	def add_css_resource_attributes(self, css_resource_attributes: list) -> 'CSSResourceUpdate':
		"""
		Add many CSSResourceAttribute.

		:param css_resource_attributes: List of CSSResourceAttribute
		:raises Exception:
		:returns: CSSResourceUpdate
		"""

		for e in css_resource_attributes:
			if not isinstance(e, merchantapi.model.CSSResourceAttribute):
				raise Exception('')
			self.css_resource_attributes.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CSSResourceUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CSSResourceUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CSSResourceUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.css_resource_id is not None:
			data['CSSResource_ID'] = self.css_resource_id
		elif self.edit_css_resource is not None:
			data['Edit_CSSResource'] = self.edit_css_resource
		elif self.css_resource_code is not None:
			data['CSSResource_Code'] = self.css_resource_code

		if self.css_resource_code is not None:
			data['CSSResource_Code'] = self.css_resource_code
		if self.css_resource_global is not None:
			data['CSSResource_Global'] = self.css_resource_global
		if self.css_resource_active is not None:
			data['CSSResource_Active'] = self.css_resource_active
		data['CSSResource_File_Path'] = self.css_resource_file_path
		if len(self.css_resource_attributes):
			data['CSSResource_Attributes'] = []

			for f in self.css_resource_attributes:
				data['CSSResource_Attributes'].append(f.to_dict())
		return data
