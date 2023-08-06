"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductVariant_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductVariantUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_variant: merchantapi.model.ProductVariant = None):
		"""
		ProductVariantUpdate Constructor.

		:param client: Client
		:param product_variant: ProductVariant
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.variant_id = None
		self.attributes = []
		self.parts = []
		if isinstance(product_variant, merchantapi.model.ProductVariant):
			if product_variant.get_product_id():
				self.set_product_id(product_variant.get_product_id())

			if product_variant.get_variant_id():
				self.set_variant_id(product_variant.get_variant_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Update'

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

	def get_variant_id(self) -> int:
		"""
		Get Variant_ID.

		:returns: int
		"""

		return self.variant_id

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

	def set_product_id(self, product_id: int) -> 'ProductVariantUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_variant_id(self, variant_id: int) -> 'ProductVariantUpdate':
		"""
		Set Variant_ID.

		:param variant_id: int
		:returns: ProductVariantUpdate
		"""

		self.variant_id = variant_id
		return self

	def set_attributes(self, attributes: list) -> 'ProductVariantUpdate':
		"""
		Set Attributes.

		:param attributes: {VariantAttribute[]}
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception("")
		self.attributes = attributes
		return self

	def set_parts(self, parts: list) -> 'ProductVariantUpdate':
		"""
		Set Parts.

		:param parts: {VariantPart[]}
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception("")
		self.parts = parts
		return self
	
	def add_variant_attribute(self, variant_attribute) -> 'ProductVariantUpdate':
		"""
		Add Attributes.

		:param variant_attribute: VariantAttribute 
		:raises Exception:
		:returns: {ProductVariantUpdate}
		"""

		if isinstance(variant_attribute, merchantapi.model.VariantAttribute):
			self.attributes.append(variant_attribute)
		elif isinstance(variant_attribute, dict):
			self.attributes.append(merchantapi.model.VariantAttribute(variant_attribute))
		else:
			raise Exception('Expected instance of VariantAttribute or dict')
		return self

	def add_attributes(self, attributes: list) -> 'ProductVariantUpdate':
		"""
		Add many VariantAttribute.

		:param attributes: List of VariantAttribute
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.VariantAttribute):
				raise Exception('')
			self.attributes.append(e)

		return self
	
	def add_variant_part(self, variant_part) -> 'ProductVariantUpdate':
		"""
		Add Parts.

		:param variant_part: VariantPart 
		:raises Exception:
		:returns: {ProductVariantUpdate}
		"""

		if isinstance(variant_part, merchantapi.model.VariantPart):
			self.parts.append(variant_part)
		elif isinstance(variant_part, dict):
			self.parts.append(merchantapi.model.VariantPart(variant_part))
		else:
			raise Exception('Expected instance of VariantPart or dict')
		return self

	def add_parts(self, parts: list) -> 'ProductVariantUpdate':
		"""
		Add many VariantPart.

		:param parts: List of VariantPart
		:raises Exception:
		:returns: ProductVariantUpdate
		"""

		for e in parts:
			if not isinstance(e, merchantapi.model.VariantPart):
				raise Exception('')
			self.parts.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantUpdate(self, http_response, data)

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

		if self.variant_id is not None:
			data['Variant_ID'] = self.variant_id

		if len(self.attributes):
			data['Attributes'] = []

			for f in self.attributes:
				data['Attributes'].append(f.to_dict())
		if len(self.parts):
			data['Parts'] = []

			for f in self.parts:
				data['Parts'].append(f.to_dict())
		return data
