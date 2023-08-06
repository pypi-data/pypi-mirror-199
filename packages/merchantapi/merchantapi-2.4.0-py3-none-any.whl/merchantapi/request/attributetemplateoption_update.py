"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AttributeTemplateOption_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateoption_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeTemplateOptionUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_option: merchantapi.model.AttributeTemplateOption = None):
		"""
		AttributeTemplateOptionUpdate Constructor.

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
		self.code = None
		self.prompt = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.default = None
		if isinstance(attribute_template_option, merchantapi.model.AttributeTemplateOption):
			if attribute_template_option.get_id():
				self.set_attribute_template_option_id(attribute_template_option.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateOption_Update'

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

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: str
		"""

		return self.image

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_cost(self) -> float:
		"""
		Get Cost.

		:returns: float
		"""

		return self.cost

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_default(self) -> bool:
		"""
		Get Default.

		:returns: bool
		"""

		return self.default

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_attribute_template_option_id(self, attribute_template_option_id: int) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateOption_ID.

		:param attribute_template_option_id: int
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_option_id = attribute_template_option_id
		return self

	def set_attribute_template_option_code(self, attribute_template_option_code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set AttributeTemplateOption_Code.

		:param attribute_template_option_code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.attribute_template_option_code = attribute_template_option_code
		return self

	def set_edit_attribute_template_option(self, edit_attribute_template_option: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Edit_AttributeTemplateOption.

		:param edit_attribute_template_option: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.edit_attribute_template_option = edit_attribute_template_option
		return self

	def set_code(self, code: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.prompt = prompt
		return self

	def set_image(self, image: str) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateOptionUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateOptionUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateOptionUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateOptionUpdate
		"""

		self.weight = weight
		return self

	def set_default(self, default: bool) -> 'AttributeTemplateOptionUpdate':
		"""
		Set Default.

		:param default: bool
		:returns: AttributeTemplateOptionUpdate
		"""

		self.default = default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateOptionUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateOptionUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateOptionUpdate(self, http_response, data)

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

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.default is not None:
			data['Default'] = self.default
		return data
