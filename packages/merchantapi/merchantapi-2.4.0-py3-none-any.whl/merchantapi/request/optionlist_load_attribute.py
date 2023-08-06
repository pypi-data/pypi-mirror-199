"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OptionList_Load_Attribute. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/optionlist_load_attribute
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OptionListLoadAttribute(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_attribute: merchantapi.model.ProductAttribute = None):
		"""
		OptionListLoadAttribute Constructor.

		:param client: Client
		:param product_attribute: ProductAttribute
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.edit_attribute = None
		self.attribute_code = None
		self.customer_id = None
		if isinstance(product_attribute, merchantapi.model.ProductAttribute):
			if product_attribute.get_product_id():
				self.set_product_id(product_attribute.get_product_id())

			if product_attribute.get_id():
				self.set_attribute_id(product_attribute.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OptionList_Load_Attribute'

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

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def set_product_id(self, product_id: int) -> 'OptionListLoadAttribute':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionListLoadAttribute
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionListLoadAttribute':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionListLoadAttribute
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionListLoadAttribute':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionListLoadAttribute
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionListLoadAttribute':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionListLoadAttribute
		"""

		self.attribute_id = attribute_id
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionListLoadAttribute':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionListLoadAttribute
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionListLoadAttribute':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionListLoadAttribute
		"""

		self.attribute_code = attribute_code
		return self

	def set_customer_id(self, customer_id: int) -> 'OptionListLoadAttribute':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OptionListLoadAttribute
		"""

		self.customer_id = customer_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionListLoadAttribute':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionListLoadAttribute':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionListLoadAttribute(self, http_response, data)

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

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		return data
