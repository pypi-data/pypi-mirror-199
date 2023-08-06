"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AttributeTemplateAttribute_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeTemplateAttributeUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, attribute_template_attribute: merchantapi.model.AttributeTemplateAttribute = None):
		"""
		AttributeTemplateAttributeUpdate Constructor.

		:param client: Client
		:param attribute_template_attribute: AttributeTemplateAttribute
		"""

		super().__init__(client)
		self.attribute_template_id = None
		self.attribute_template_code = None
		self.edit_attribute_template = None
		self.attribute_template_attribute_id = None
		self.attribute_template_attribute_code = None
		self.edit_attribute_template_attribute = None
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
		if isinstance(attribute_template_attribute, merchantapi.model.AttributeTemplateAttribute):
			if attribute_template_attribute.get_id():
				self.set_attribute_template_attribute_id(attribute_template_attribute.get_id())
			elif attribute_template_attribute.get_code():
				self.set_attribute_template_attribute_code(attribute_template_attribute.get_code())
			elif attribute_template_attribute.get_code():
				self.set_edit_attribute_template_attribute(attribute_template_attribute.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplateAttribute_Update'

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

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set AttributeTemplateAttribute_Code.

		:param attribute_template_attribute_code: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.attribute_template_attribute_code = attribute_template_attribute_code
		return self

	def set_edit_attribute_template_attribute(self, edit_attribute_template_attribute: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Edit_AttributeTemplateAttribute.

		:param edit_attribute_template_attribute: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.edit_attribute_template_attribute = edit_attribute_template_attribute
		return self

	def set_code(self, code: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Type.

		:param type: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Image.

		:param image: str
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Price.

		:param price: float
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeTemplateAttributeUpdate':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeTemplateAttributeUpdate
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateAttributeUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateAttributeUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateAttributeUpdate(self, http_response, data)

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

		data['Code'] = self.code
		if self.prompt is not None:
			data['Prompt'] = self.prompt
		if self.type is not None:
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
