"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductVariantList_Load_Product. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariantlist_load_product
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductVariantListLoadProduct(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantListLoadProduct Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.product_sku = None
		self.include_default_variant = None
		self.limits = []
		self.exclusions = []
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())
			elif product.get_sku():
				self.set_product_sku(product.get_sku())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariantList_Load_Product'

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

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_include_default_variant(self) -> bool:
		"""
		Get Include_Default_Variant.

		:returns: bool
		"""

		return self.include_default_variant

	def get_limits(self) -> list:
		"""
		Get Limits.

		:returns: List of ProductVariantLimit
		"""

		return self.limits

	def get_exclusions(self) -> list:
		"""
		Get Exclusions.

		:returns: List of ProductVariantExclusion
		"""

		return self.exclusions

	def set_product_id(self, product_id: int) -> 'ProductVariantListLoadProduct':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantListLoadProduct
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantListLoadProduct':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantListLoadProduct
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantListLoadProduct':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantListLoadProduct
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductVariantListLoadProduct':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductVariantListLoadProduct
		"""

		self.product_sku = product_sku
		return self

	def set_include_default_variant(self, include_default_variant: bool) -> 'ProductVariantListLoadProduct':
		"""
		Set Include_Default_Variant.

		:param include_default_variant: bool
		:returns: ProductVariantListLoadProduct
		"""

		self.include_default_variant = include_default_variant
		return self

	def set_limits(self, limits: list) -> 'ProductVariantListLoadProduct':
		"""
		Set Limits.

		:param limits: {ProductVariantLimit[]}
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in limits:
			if not isinstance(e, merchantapi.model.ProductVariantLimit):
				raise Exception("")
		self.limits = limits
		return self

	def set_exclusions(self, exclusions: list) -> 'ProductVariantListLoadProduct':
		"""
		Set Exclusions.

		:param exclusions: {ProductVariantExclusion[]}
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.ProductVariantExclusion):
				raise Exception("")
		self.exclusions = exclusions
		return self
	
	def add_limit(self, limit) -> 'ProductVariantListLoadProduct':
		"""
		Add Limits.

		:param limit: ProductVariantLimit 
		:raises Exception:
		:returns: {ProductVariantListLoadProduct}
		"""

		if isinstance(limit, merchantapi.model.ProductVariantLimit):
			self.limits.append(limit)
		elif isinstance(limit, dict):
			self.limits.append(merchantapi.model.ProductVariantLimit(limit))
		else:
			raise Exception('Expected instance of ProductVariantLimit or dict')
		return self

	def add_limits(self, limits: list) -> 'ProductVariantListLoadProduct':
		"""
		Add many ProductVariantLimit.

		:param limits: List of ProductVariantLimit
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in limits:
			if not isinstance(e, merchantapi.model.ProductVariantLimit):
				raise Exception('')
			self.limits.append(e)

		return self
	
	def add_exclusion(self, exclusion) -> 'ProductVariantListLoadProduct':
		"""
		Add Exclusions.

		:param exclusion: ProductVariantExclusion 
		:raises Exception:
		:returns: {ProductVariantListLoadProduct}
		"""

		if isinstance(exclusion, merchantapi.model.ProductVariantExclusion):
			self.exclusions.append(exclusion)
		elif isinstance(exclusion, dict):
			self.exclusions.append(merchantapi.model.ProductVariantExclusion(exclusion))
		else:
			raise Exception('Expected instance of ProductVariantExclusion or dict')
		return self

	def add_exclusions(self, exclusions: list) -> 'ProductVariantListLoadProduct':
		"""
		Add many ProductVariantExclusion.

		:param exclusions: List of ProductVariantExclusion
		:raises Exception:
		:returns: ProductVariantListLoadProduct
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.ProductVariantExclusion):
				raise Exception('')
			self.exclusions.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantListLoadProduct':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantListLoadProduct':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantListLoadProduct(self, http_response, data)

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
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		if self.include_default_variant is not None:
			data['Include_Default_Variant'] = self.include_default_variant
		if len(self.limits):
			data['Limits'] = []

			for f in self.limits:
				data['Limits'].append(f.to_dict())
		if len(self.exclusions):
			data['Exclusions'] = []

			for f in self.exclusions:
				data['Exclusions'].append(f.to_dict())
		return data
