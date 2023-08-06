"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Attribute_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
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
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

			self.set_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Insert'

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

	def set_product_id(self, product_id: int) -> 'AttributeInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeInsert
		"""

		self.edit_product = edit_product
		return self

	def set_code(self, code: str) -> 'AttributeInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeInsert
		"""

		self.prompt = prompt
		return self

	def set_type(self, type: str) -> 'AttributeInsert':
		"""
		Set Type.

		:param type: str
		:returns: AttributeInsert
		"""

		self.type = type
		return self

	def set_image(self, image: str) -> 'AttributeInsert':
		"""
		Set Image.

		:param image: str
		:returns: AttributeInsert
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'AttributeInsert':
		"""
		Set Price.

		:param price: float
		:returns: AttributeInsert
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'AttributeInsert':
		"""
		Set Cost.

		:param cost: float
		:returns: AttributeInsert
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'AttributeInsert':
		"""
		Set Weight.

		:param weight: float
		:returns: AttributeInsert
		"""

		self.weight = weight
		return self

	def set_copy(self, copy: bool) -> 'AttributeInsert':
		"""
		Set Copy.

		:param copy: bool
		:returns: AttributeInsert
		"""

		self.copy = copy
		return self

	def set_required(self, required: bool) -> 'AttributeInsert':
		"""
		Set Required.

		:param required: bool
		:returns: AttributeInsert
		"""

		self.required = required
		return self

	def set_inventory(self, inventory: bool) -> 'AttributeInsert':
		"""
		Set Inventory.

		:param inventory: bool
		:returns: AttributeInsert
		"""

		self.inventory = inventory
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.product_code is not None:
			data['Product_Code'] = self.product_code
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
