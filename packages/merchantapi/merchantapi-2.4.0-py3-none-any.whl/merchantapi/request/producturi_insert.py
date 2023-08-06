"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/producturi_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductURIInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.uri = None
		self.status = None
		self.canonical = None
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductURI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

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

	def set_uri(self, uri: str) -> 'ProductURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: ProductURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'ProductURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: ProductURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'ProductURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: ProductURIInsert
		"""

		self.canonical = canonical
		return self

	def set_product_id(self, product_id: int) -> 'ProductURIInsert':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductURIInsert
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductURIInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductURIInsert
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductURIInsert':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductURIInsert
		"""

		self.edit_product = edit_product
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductURIInsert(self, http_response, data)

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

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data
