"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductKit_Update_Parts. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productkit_update_parts
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductKitUpdateParts(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductKitUpdateParts Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.attribute_template_attribute_id = None
		self.option_id = None
		self.parts = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductKit_Update_Parts'

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

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get AttributeTemplateAttribute_ID.

		:returns: int
		"""

		return self.attribute_template_attribute_id

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_parts(self) -> list:
		"""
		Get Parts.

		:returns: List of KitPart
		"""

		return self.parts

	def set_product_id(self, product_id: int) -> 'ProductKitUpdateParts':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductKitUpdateParts
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductKitUpdateParts':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductKitUpdateParts
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductKitUpdateParts':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductKitUpdateParts
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'ProductKitUpdateParts':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: ProductKitUpdateParts
		"""

		self.attribute_id = attribute_id
		return self

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'ProductKitUpdateParts':
		"""
		Set AttributeTemplateAttribute_ID.

		:param attribute_template_attribute_id: int
		:returns: ProductKitUpdateParts
		"""

		self.attribute_template_attribute_id = attribute_template_attribute_id
		return self

	def set_option_id(self, option_id: int) -> 'ProductKitUpdateParts':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: ProductKitUpdateParts
		"""

		self.option_id = option_id
		return self

	def set_parts(self, parts: list) -> 'ProductKitUpdateParts':
		"""
		Set Parts.

		:param parts: {KitPart[]}
		:raises Exception:
		:returns: ProductKitUpdateParts
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.KitPart):
				raise Exception("")
		self.parts = parts
		return self
	
	def add_kit_part(self, kit_part) -> 'ProductKitUpdateParts':
		"""
		Add Parts.

		:param kit_part: KitPart 
		:raises Exception:
		:returns: {ProductKitUpdateParts}
		"""

		if isinstance(kit_part, merchantapi.model.KitPart):
			self.parts.append(kit_part)
		elif isinstance(kit_part, dict):
			self.parts.append(merchantapi.model.KitPart(kit_part))
		else:
			raise Exception('Expected instance of KitPart or dict')
		return self

	def add_parts(self, parts: list) -> 'ProductKitUpdateParts':
		"""
		Add many KitPart.

		:param parts: List of KitPart
		:raises Exception:
		:returns: ProductKitUpdateParts
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.KitPart):
				raise Exception('')
			self.parts.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductKitUpdateParts':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductKitUpdateParts':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductKitUpdateParts(self, http_response, data)

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

		if self.attribute_template_attribute_id is not None:
			data['AttributeTemplateAttribute_ID'] = self.attribute_template_attribute_id

		if self.option_id is not None:
			data['Option_ID'] = self.option_id

		if len(self.parts):
			data['Parts'] = []

			for f in self.parts:
				data['Parts'].append(f.to_dict())
		return data
