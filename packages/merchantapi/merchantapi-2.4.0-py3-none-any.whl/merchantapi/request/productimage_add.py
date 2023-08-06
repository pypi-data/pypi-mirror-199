"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductImage_Add. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productimage_add
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductImageAdd(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductImageAdd Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_code = None
		self.product_id = None
		self.edit_product = None
		self.product_sku = None
		self.filepath = None
		self.image_type_id = None
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

		return 'ProductImage_Add'

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

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

	def get_filepath(self) -> str:
		"""
		Get Filepath.

		:returns: str
		"""

		return self.filepath

	def get_image_type_id(self) -> int:
		"""
		Get ImageType_ID.

		:returns: int
		"""

		return self.image_type_id

	def set_product_code(self, product_code: str) -> 'ProductImageAdd':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductImageAdd
		"""

		self.product_code = product_code
		return self

	def set_product_id(self, product_id: int) -> 'ProductImageAdd':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductImageAdd
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductImageAdd':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductImageAdd
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductImageAdd':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductImageAdd
		"""

		self.product_sku = product_sku
		return self

	def set_filepath(self, filepath: str) -> 'ProductImageAdd':
		"""
		Set Filepath.

		:param filepath: str
		:returns: ProductImageAdd
		"""

		self.filepath = filepath
		return self

	def set_image_type_id(self, image_type_id: int) -> 'ProductImageAdd':
		"""
		Set ImageType_ID.

		:param image_type_id: int
		:returns: ProductImageAdd
		"""

		self.image_type_id = image_type_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductImageAdd':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductImageAdd':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductImageAdd(self, http_response, data)

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
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Filepath'] = self.filepath
		data['ImageType_ID'] = self.image_type_id
		return data
