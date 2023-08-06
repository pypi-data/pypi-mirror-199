"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AttributeAndOptionList_Load_Product. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributeandoptionlist_load_product
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeAndOptionListLoadProduct(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeAndOptionListLoadProduct Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.customer_id = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())

			self.set_product_code(product.get_code())
			self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeAndOptionList_Load_Product'

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

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def set_product_id(self, product_id: int) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.edit_product = edit_product
		return self

	def set_customer_id(self, customer_id: int) -> 'AttributeAndOptionListLoadProduct':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: AttributeAndOptionListLoadProduct
		"""

		self.customer_id = customer_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeAndOptionListLoadProduct':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeAndOptionListLoadProduct':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeAndOptionListLoadProduct(self, http_response, data)

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

		if self.product_code is not None:
			data['Product_Code'] = self.product_code
		if self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		return data
