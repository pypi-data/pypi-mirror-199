"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AttributeTemplateOption_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoption_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeTemplateOptionDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_option: merchantapi.model.AttributeTemplateOption = None):
		"""
		AttributeTemplateOptionDelete Constructor.

		:param client: Client
		:param attribute_template_option: AttributeTemplateOption
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
		self.attribute_template_option_id = None
		self.attribute_template_option_code = None
		self.edit_attribute_template_option = None
		if isinstance(attribute_template_option, merchantapi.model.AttributeTemplateOption):
			if attribute_template_option.get_id():
				self.set_attribute_template_option_id(attribute_template_option.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOption_Delete'

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get AttributeTemplateAttribute_Code.

		:returns: str
		"""

		return self.attribute_template_attribute_code

	def get_edit_attribute_template_attribute(self) -> str:
		"""
		Get Edit_AttributeTemplateAttribute.

		:returns: str
		"""

		return self.edit_attribute_template_attribute

	def get_attribute_template_option_id(self) -> int:
		"""
		Get AttributeTemplateOption_ID.

		:returns: int
		"""

		return self.attribute_template_option_id

	def get_attribute_template_option_code(self) -> str:
		"""
		Get AttributeTemplateOption_Code.

		:returns: str
		"""

		return self.attribute_template_option_code

	def get_edit_attribute_template_option(self) -> str:
		"""
		Get Edit_AttributeTemplateOption.

		:returns: str
		"""

		return self.edit_attribute_template_option

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_attribute_template_option_id(self, attribute_template_option_id: int) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateOption_ID.

		:param attribute_template_option_id: int
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_option_id = attribute_template_option_id
		return self

	def set_attribute_template_option_code(self, attribute_template_option_code: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set AttributeTemplateOption_Code.

		:param attribute_template_option_code: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.attribute_template_option_code = attribute_template_option_code
		return self

	def set_edit_attribute_template_option(self, edit_attribute_template_option: str) -> 'AttributeTemplateOptionDelete':
		"""
		Set Edit_AttributeTemplateOption.

		:param edit_attribute_template_option: str
		:returns: AttributeTemplateOptionDelete
		"""

		self.edit_attribute_template_option = edit_attribute_template_option
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id
		elif self.attribute_template_attribute_code is not None:
			data['AttributeTemplateAttribute_Code'] = self.attribute_template_attribute_code
		elif self.edit_attribute_template_attribute is not None:
			data['Edit_AttributeTemplateAttribute'] = self.edit_attribute_template_attribute

		if self.attribute_template_option_id is not None:
			data['AttributeTemplateOption_ID'] = self.attribute_template_option_id
		elif self.attribute_template_option_code is not None:
			data['AttributeTemplateOption_Code'] = self.attribute_template_option_code
		elif self.edit_attribute_template_option is not None:
			data['Edit_AttributeTemplateOption'] = self.edit_attribute_template_option

		return data
