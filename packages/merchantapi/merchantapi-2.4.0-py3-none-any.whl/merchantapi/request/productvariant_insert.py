"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductVariant_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductVariantInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attributes = []
		self.parts = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Insert'

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

	def get_attributes(self) -> list:
		"""
		Get Attributes.

		:returns: List of VariantAttribute
		"""

		return self.attributes

	def get_parts(self) -> list:
		"""
		Get Parts.

		:returns: List of VariantPart
		"""

		return self.parts

	def set_product_id(self, product_id: int) -> 'ProductVariantInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantInsert
		"""

		self.edit_product = edit_product
		return self

	def set_attributes(self, attributes: list) -> 'ProductVariantInsert':
		"""
		Set Attributes.

		:param attributes: {VariantAttribute[]}
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception("")
		self.attributes = attributes
		return self

	def set_parts(self, parts: list) -> 'ProductVariantInsert':
		"""
		Set Parts.

		:param parts: {VariantPart[]}
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception("")
		self.parts = parts
		return self
	
	def add_variant_attribute(self, variant_attribute) -> 'ProductVariantInsert':
		"""
		Add Attributes.

		:param variant_attribute: VariantAttribute 
		:raises Exception:
		:returns: {ProductVariantInsert}
		"""

		if isinstance(variant_attribute, merchantapi.model.VariantAttribute):
			self.attributes.append(variant_attribute)
		elif isinstance(variant_attribute, dict):
			self.attributes.append(merchantapi.model.VariantAttribute(variant_attribute))
		else:
			raise Exception('Expected instance of VariantAttribute or dict')
		return self

	def add_attributes(self, attributes: list) -> 'ProductVariantInsert':
		"""
		Add many VariantAttribute.

		:param attributes: List of VariantAttribute
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception('')
			self.attributes.append(e)

		return self
	
	def add_variant_part(self, variant_part) -> 'ProductVariantInsert':
		"""
		Add Parts.

		:param variant_part: VariantPart 
		:raises Exception:
		:returns: {ProductVariantInsert}
		"""

		if isinstance(variant_part, merchantapi.model.VariantPart):
			self.parts.append(variant_part)
		elif isinstance(variant_part, dict):
			self.parts.append(merchantapi.model.VariantPart(variant_part))
		else:
			raise Exception('Expected instance of VariantPart or dict')
		return self

	def add_parts(self, parts: list) -> 'ProductVariantInsert':
		"""
		Add many VariantPart.

		:param parts: List of VariantPart
		:raises Exception:
		:returns: ProductVariantInsert
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception('')
			self.parts.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantInsert(self, http_response, data)

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

		if len(self.attributes):
			data['Attributes'] = []

			for f in self.attributes:
				data['Attributes'].append(f.to_dict())
		if len(self.parts):
			data['Parts'] = []

			for f in self.parts:
				data['Parts'].append(f.to_dict())
		return data
