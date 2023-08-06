"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Attribute_Load_Code. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_load_code
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeLoadCode(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeLoadCode Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.customer_id = None
		self.attribute_code = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Attribute_Load_Code'

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

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def set_product_id(self, product_id: int) -> 'AttributeLoadCode':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeLoadCode
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AttributeLoadCode':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeLoadCode
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeLoadCode':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeLoadCode
		"""

		self.edit_product = edit_product
		return self

	def set_customer_id(self, customer_id: int) -> 'AttributeLoadCode':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: AttributeLoadCode
		"""

		self.customer_id = customer_id
		return self

	def set_attribute_code(self, attribute_code: str) -> 'AttributeLoadCode':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: AttributeLoadCode
		"""

		self.attribute_code = attribute_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeLoadCode':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeLoadCode':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeLoadCode(self, http_response, data)

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

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		data['Attribute_Code'] = self.attribute_code
		return data
