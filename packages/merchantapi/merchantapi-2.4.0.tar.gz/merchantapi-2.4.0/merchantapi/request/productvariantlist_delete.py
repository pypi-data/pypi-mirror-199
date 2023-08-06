"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductVariantList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariantlist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductVariantListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantListDelete Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.product_variant_ids = []
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

		return 'ProductVariantList_Delete'

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

	def get_product_variant_ids(self):
		"""
		Get ProductVariant_IDs.

		:returns: list
		"""

		return self.product_variant_ids

	def set_product_id(self, product_id: int) -> 'ProductVariantListDelete':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantListDelete
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantListDelete':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantListDelete
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantListDelete':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantListDelete
		"""

		self.edit_product = edit_product
		return self
	
	def add_variant_id(self, variant_id) -> 'ProductVariantListDelete':
		"""
		Add ProductVariant_IDs.

		:param variant_id: int
		:returns: {ProductVariantListDelete}
		"""

		self.product_variant_ids.append(variant_id)
		return self

	def add_product_variant(self, product_variant: merchantapi.model.ProductVariant) -> 'ProductVariantListDelete':
		"""
		Add ProductVariant model.

		:param product_variant: ProductVariant
		:raises Exception:
		:returns: ProductVariantListDelete
		"""
		if not isinstance(product_variant, merchantapi.model.ProductVariant):
			raise Exception('Expected an instance of ProductVariant')

		if product_variant.get_variant_id():
			self.product_variant_ids.append(product_variant.get_variant_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantListDelete(self, http_response, data)

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

		data['ProductVariant_IDs'] = self.product_variant_ids
		return data
