"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Attribute_CopyTemplate. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attribute_copytemplate
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeCopyTemplate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		AttributeCopyTemplate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.attribute_template_id = None
		self.edit_attribute_template = None
		self.attribute_template_code = None
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

		return 'Attribute_CopyTemplate'

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

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_attribute_template_id(self) -> int:
		"""
		Get AttributeTemplate_ID.

		:returns: int
		"""

		return self.attribute_template_id

	def get_edit_attribute_template(self) -> str:
		"""
		Get Edit_AttributeTemplate.

		:returns: str
		"""

		return self.edit_attribute_template

	def get_attribute_template_code(self) -> str:
		"""
		Get AttributeTemplate_Code.

		:returns: str
		"""

		return self.attribute_template_code

	def set_product_id(self, product_id: int) -> 'AttributeCopyTemplate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AttributeCopyTemplate
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'AttributeCopyTemplate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AttributeCopyTemplate
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'AttributeCopyTemplate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AttributeCopyTemplate
		"""

		self.product_code = product_code
		return self

	def set_attribute_template_id(self, attribute_template_id: int) -> 'AttributeCopyTemplate':
		"""
		Set AttributeTemplate_ID.

		:param attribute_template_id: int
		:returns: AttributeCopyTemplate
		"""

		self.attribute_template_id = attribute_template_id
		return self

	def set_edit_attribute_template(self, edit_attribute_template: str) -> 'AttributeCopyTemplate':
		"""
		Set Edit_AttributeTemplate.

		:param edit_attribute_template: str
		:returns: AttributeCopyTemplate
		"""

		self.edit_attribute_template = edit_attribute_template
		return self

	def set_attribute_template_code(self, attribute_template_code: str) -> 'AttributeCopyTemplate':
		"""
		Set AttributeTemplate_Code.

		:param attribute_template_code: str
		:returns: AttributeCopyTemplate
		"""

		self.attribute_template_code = attribute_template_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeCopyTemplate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeCopyTemplate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeCopyTemplate(self, http_response, data)

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

		if self.attribute_template_id is not None:
			data['AttributeTemplate_ID'] = self.attribute_template_id
		elif self.edit_attribute_template is not None:
			data['Edit_AttributeTemplate'] = self.edit_attribute_template
		elif self.attribute_template_code is not None:
			data['AttributeTemplate_Code'] = self.attribute_template_code

		return data
