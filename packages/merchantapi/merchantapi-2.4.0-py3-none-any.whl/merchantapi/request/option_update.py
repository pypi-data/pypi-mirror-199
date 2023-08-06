"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Option_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OptionUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_option: merchantapi.model.ProductOption = None):
		"""
		OptionUpdate Constructor.

		:param client: Client
		:param product_option: ProductOption
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.option_id = None
		self.option_code = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		self.code = None
		self.prompt = None
		self.image = None
		self.price = None
		self.cost = None
		self.weight = None
		self.default = None
		if isinstance(product_option, merchantapi.model.ProductOption):
			if product_option.get_product_id():
				self.set_product_id(product_option.get_product_id())

			if product_option.get_attribute_id():
				self.set_attribute_id(product_option.get_attribute_id())

			if product_option.get_id():
				self.set_option_id(product_option.get_id())
			elif product_option.get_code():
				self.set_option_code(product_option.get_code())

			self.set_code(product_option.get_code())
			self.set_prompt(product_option.get_prompt())
			self.set_image(product_option.get_image())
			self.set_price(product_option.get_price())
			self.set_cost(product_option.get_cost())
			self.set_weight(product_option.get_weight())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Update'

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

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

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

	def set_product_id(self, product_id: int) -> 'OptionUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_option_id(self, option_id: int) -> 'OptionUpdate':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: OptionUpdate
		"""

		self.option_id = option_id
		return self

	def set_option_code(self, option_code: str) -> 'OptionUpdate':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionUpdate
		"""

		self.option_code = option_code
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionUpdate':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionUpdate
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionUpdate':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionUpdate
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionUpdate':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionUpdate
		"""

		self.attribute_code = attribute_code
		return self

	def set_code(self, code: str) -> 'OptionUpdate':
		"""
		Set Code.

		:param code: str
		:returns: OptionUpdate
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'OptionUpdate':
		"""
		Set Prompt.

		:param prompt: str
		:returns: OptionUpdate
		"""

		self.prompt = prompt
		return self

	def set_image(self, image: str) -> 'OptionUpdate':
		"""
		Set Image.

		:param image: str
		:returns: OptionUpdate
		"""

		self.image = image
		return self

	def set_price(self, price: float) -> 'OptionUpdate':
		"""
		Set Price.

		:param price: float
		:returns: OptionUpdate
		"""

		self.price = price
		return self

	def set_cost(self, cost: float) -> 'OptionUpdate':
		"""
		Set Cost.

		:param cost: float
		:returns: OptionUpdate
		"""

		self.cost = cost
		return self

	def set_weight(self, weight: float) -> 'OptionUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: OptionUpdate
		"""

		self.weight = weight
		return self

	def set_default(self, default: bool) -> 'OptionUpdate':
		"""
		Set Default.

		:param default: bool
		:returns: OptionUpdate
		"""

		self.default = default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionUpdate(self, http_response, data)

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
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.option_id is not None:
			data['Option_ID'] = self.option_id
		elif self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.code is not None:
			data['Code'] = self.code
		if self.prompt is not None:
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
