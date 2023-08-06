"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Option_Load_Code. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_load_code
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OptionLoadCode(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OptionLoadCode Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.attribute_id = None
		self.attribute_code = None
		self.edit_attribute = None
		self.option_code = None
		self.customer_id = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Load_Code'

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

	def get_attribute_code(self) -> str:
		"""
		Get Attribute_Code.

		:returns: str
		"""

		return self.attribute_code

	def get_edit_attribute(self) -> str:
		"""
		Get Edit_Attribute.

		:returns: str
		"""

		return self.edit_attribute

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def set_product_id(self, product_id: int) -> 'OptionLoadCode':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: OptionLoadCode
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'OptionLoadCode':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: OptionLoadCode
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'OptionLoadCode':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: OptionLoadCode
		"""

		self.edit_product = edit_product
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionLoadCode':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionLoadCode
		"""

		self.attribute_id = attribute_id
		return self

	def set_attribute_code(self, attribute_code: str) -> 'OptionLoadCode':
		"""
		Set Attribute_Code.

		:param attribute_code: str
		:returns: OptionLoadCode
		"""

		self.attribute_code = attribute_code
		return self

	def set_edit_attribute(self, edit_attribute: str) -> 'OptionLoadCode':
		"""
		Set Edit_Attribute.

		:param edit_attribute: str
		:returns: OptionLoadCode
		"""

		self.edit_attribute = edit_attribute
		return self

	def set_option_code(self, option_code: str) -> 'OptionLoadCode':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionLoadCode
		"""

		self.option_code = option_code
		return self

	def set_customer_id(self, customer_id: int) -> 'OptionLoadCode':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OptionLoadCode
		"""

		self.customer_id = customer_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionLoadCode':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionLoadCode':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionLoadCode(self, http_response, data)

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

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id
		elif self.attribute_code is not None:
			data['Attribute_Code'] = self.attribute_code
		elif self.edit_attribute is not None:
			data['Edit_Attribute'] = self.edit_attribute

		if self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		return data
