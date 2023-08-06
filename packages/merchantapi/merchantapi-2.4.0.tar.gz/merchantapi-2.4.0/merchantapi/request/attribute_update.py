"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Attribute_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_attribute: merchantapi.model.ProductAttribute = None):
		"""
		AttributeUpdate Constructor.

		:param client: Client
		:param product_attribute: ProductAttribute
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
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
		if isinstance(product_attribute, merchantapi.model.ProductAttribute):
			if product_attribute.get_product_id():
				self.set_product_id(product_attribute.get_product_id())

			if product_attribute.get_id():
				self.set_attribute_id(product_attribute.get_id())
			elif product_attribute.get_code():
				self.set_edit_attribute(product_attribute.get_code())
			elif product_attribute.get_code():
				self.set_attribute_code(product_attribute.get_code())

			self.set_edit_attribute(product_attribute.get_code())
			self.set_code(product_attribute.get_code())
			self.set_prompt(product_attribute.get_prompt())
			self.set_type(product_attribute.get_type())
			self.set_image(product_attribute.get_image())
			self.set_price(product_attribute.get_price())
			self.set_cost(product_attribute.get_cost())
			self.set_weight(product_attribute.get_weight())
			self.set_required(product_attribute.get_required())
			self.set_inventory(product_attribute.get_inventory())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

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

	def set_product_id(self, product_id: int) -> 'AttributeUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'AttributeUpdate':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: AttributeUpdate
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'AttributeUpdate':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: AttributeUpdate
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'AttributeUpdate':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: AttributeUpdate
		"""

		self.attribute_code = attribute_code
		return self

	def set_code(self, code: str) -> 'AttributeUpdate':
		"""
		Set Code.

		:param code: str
		:returns: AttributeUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeUpdate
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeUpdate':
		"""
		Set Type.

		:param type: str
		:returns: AttributeUpdate
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeUpdate':
		"""
		Set Image.

		:param image: str
		:returns: AttributeUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeUpdate':
		"""
		Set Price.

		:param price: float
		:returns: AttributeUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeUpdate
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeUpdate':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeUpdate
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeUpdate':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeUpdate
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeUpdate':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeUpdate
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		if self.code is not None:
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
