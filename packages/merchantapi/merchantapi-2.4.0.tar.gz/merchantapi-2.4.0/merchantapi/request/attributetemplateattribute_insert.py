"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AttributeTemplateAttribute_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeTemplateAttributeInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template: merchantapi.model.AttributeTemplate = None):
		"""
		AttributeTemplateAttributeInsert Constructor.

		:param client: Client
		:param attribute_template: AttributeTemplate
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.code = None
		self.prompt = None
		self.type = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.copy = None
		self.required = None
		self.inventory = None
		if isinstance(attribute_template, merchantapi.model.AttributeTemplate):
			if attribute_template.get_id():
				self.set_attribute_template_id(attribute_template.get_id())
			elif attribute_template.get_code():
				self.set_attribute_template_code(attribute_template.get_code())
			elif attribute_template.get_code():
				self.set_edit_attribute_template(attribute_template.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateAttribute_Insert'

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

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: str
		"""

		return self.type

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

	def get_copy(self) -> bool:
		"""
		Get Copy.

		:returns: bool
		"""

		return self.copy

	def get_required(self) -> bool:
		"""
		Get Required.

		:returns: bool
		"""

		return self.required

	def get_inventory(self) -> bool:
		"""
		Get Inventory.

		:returns: bool
		"""

		return self.inventory

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateAttributeInsert':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateAttributeInsert
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_code(self, code: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Type.

		:param type: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateAttributeInsert
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateAttributeInsert
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateAttributeInsert
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateAttributeInsert
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeTemplateAttributeInsert
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeTemplateAttributeInsert
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeTemplateAttributeInsert':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeTemplateAttributeInsert
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateAttributeInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateAttributeInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateAttributeInsert(self, http_response, data)

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

		data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		data['Type'] = self.type
		if self.image is not None:
			data['Image'] = self.image
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.copy is not None:
			data['Copy'] = self.copy
		if self.required is not None:
			data['Required'] = self.required
		if self.inventory is not None:
			data['Inventory'] = self.inventory
		return data
