"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductKit_Generate_Variants. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productkit_generate_variants
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductKitGenerateVariants(merchantapi.abstract.Request):
	# VARIANT_PRICING_METHOD constants.
	VARIANT_PRICING_METHOD_MASTER = 'master'
	VARIANT_PRICING_METHOD_SPECIFIC = 'specific'
	VARIANT_PRICING_METHOD_SUM = 'sum'

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductKitGenerateVariants Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.pricing_method = None
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

		return 'ProductKit_Generate_Variants'

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

	def get_pricing_method(self) -> str:
		"""
		Get Pricing_Method.

		:returns: str
		"""

		return self.pricing_method

	def set_product_id(self, product_id: int) -> 'ProductKitGenerateVariants':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductKitGenerateVariants
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductKitGenerateVariants':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductKitGenerateVariants
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductKitGenerateVariants':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductKitGenerateVariants
		"""

		self.edit_product = edit_product
		return self

	def set_pricing_method(self, pricing_method: str) -> 'ProductKitGenerateVariants':
		"""
		Set Pricing_Method.

		:param pricing_method: str
		:returns: ProductKitGenerateVariants
		"""

		self.pricing_method = pricing_method
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductKitGenerateVariants':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductKitGenerateVariants':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductKitGenerateVariants(self, http_response, data)

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

		data['Pricing_Method'] = self.pricing_method
		return data
