"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CSSResource_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/cssresource_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CSSResourceDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, css_resource: merchantapi.model.CSSResource = None):
		"""
		CSSResourceDelete Constructor.

		:param client: Client
		:param css_resource: CSSResource
		"""

		super().__init__(client)
		self.css_resource_id = None
		self.edit_css_resource = None
		self.css_resource_code = None
		if isinstance(css_resource, merchantapi.model.CSSResource):
			if css_resource.get_id():
				self.set_css_resource_id(css_resource.get_id())
			elif css_resource.get_code():
				self.set_edit_css_resource(css_resource.get_code())
			elif css_resource.get_code():
				self.set_css_resource_code(css_resource.get_code())

			self.set_css_resource_code(css_resource.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CSSResource_Delete'

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

	def set_css_resource_id(self, css_resource_id: int) -> 'CSSResourceDelete':
		"""
		Set CSSResource_ID.

		:param css_resource_id: int
		:returns: CSSResourceDelete
		"""

		self.css_resource_id = css_resource_id
		return self

	def set_edit_css_resource(self, edit_css_resource: str) -> 'CSSResourceDelete':
		"""
		Set Edit_CSSResource.

		:param edit_css_resource: str
		:returns: CSSResourceDelete
		"""

		self.edit_css_resource = edit_css_resource
		return self

	def set_css_resource_code(self, css_resource_code: str) -> 'CSSResourceDelete':
		"""
		Set CSSResource_Code.

		:param css_resource_code: str
		:returns: CSSResourceDelete
		"""

		self.css_resource_code = css_resource_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CSSResourceDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CSSResourceDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CSSResourceDelete(self, http_response, data)

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
		return data
