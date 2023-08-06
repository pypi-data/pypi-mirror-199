"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Product_Copy. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/product_copy
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductCopy(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductCopy Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_copy_session_id = None
		self.copy_product_rules_id = None
		self.copy_product_rules_name = None
		self.source_product_id = None
		self.source_product_code = None
		self.destination_product_code = None
		self.destination_product_name = None
		self.destination_product_sku = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_source_product_id(product.get_id())
			elif product.get_code():
				self.set_source_product_code(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Product_Copy'

	def get_product_copy_session_id(self) -> str:
		"""
		Get Product_Copy_Session_ID.

		:returns: str
		"""

		return self.product_copy_session_id

	def get_copy_product_rules_id(self) -> int:
		"""
		Get CopyProductRules_ID.

		:returns: int
		"""

		return self.copy_product_rules_id

	def get_copy_product_rules_name(self) -> str:
		"""
		Get CopyProductRules_Name.

		:returns: str
		"""

		return self.copy_product_rules_name

	def get_source_product_id(self) -> int:
		"""
		Get Source_Product_ID.

		:returns: int
		"""

		return self.source_product_id

	def get_source_product_code(self) -> str:
		"""
		Get Source_Product_Code.

		:returns: str
		"""

		return self.source_product_code

	def get_destination_product_code(self) -> str:
		"""
		Get destination_product_code.

		:returns: str
		"""

		return self.destination_product_code

	def get_destination_product_name(self) -> str:
		"""
		Get destination_product_name.

		:returns: str
		"""

		return self.destination_product_name

	def get_destination_product_sku(self) -> str:
		"""
		Get destination_product_sku.

		:returns: str
		"""

		return self.destination_product_sku

	def set_product_copy_session_id(self, product_copy_session_id: str) -> 'ProductCopy':
		"""
		Set Product_Copy_Session_ID.

		:param product_copy_session_id: str
		:returns: ProductCopy
		"""

		self.product_copy_session_id = product_copy_session_id
		return self

	def set_copy_product_rules_id(self, copy_product_rules_id: int) -> 'ProductCopy':
		"""
		Set CopyProductRules_ID.

		:param copy_product_rules_id: int
		:returns: ProductCopy
		"""

		self.copy_product_rules_id = copy_product_rules_id
		return self

	def set_copy_product_rules_name(self, copy_product_rules_name: str) -> 'ProductCopy':
		"""
		Set CopyProductRules_Name.

		:param copy_product_rules_name: str
		:returns: ProductCopy
		"""

		self.copy_product_rules_name = copy_product_rules_name
		return self

	def set_source_product_id(self, source_product_id: int) -> 'ProductCopy':
		"""
		Set Source_Product_ID.

		:param source_product_id: int
		:returns: ProductCopy
		"""

		self.source_product_id = source_product_id
		return self

	def set_source_product_code(self, source_product_code: str) -> 'ProductCopy':
		"""
		Set Source_Product_Code.

		:param source_product_code: str
		:returns: ProductCopy
		"""

		self.source_product_code = source_product_code
		return self

	def set_destination_product_code(self, destination_product_code: str) -> 'ProductCopy':
		"""
		Set destination_product_code.

		:param destination_product_code: str
		:returns: ProductCopy
		"""

		self.destination_product_code = destination_product_code
		return self

	def set_destination_product_name(self, destination_product_name: str) -> 'ProductCopy':
		"""
		Set destination_product_name.

		:param destination_product_name: str
		:returns: ProductCopy
		"""

		self.destination_product_name = destination_product_name
		return self

	def set_destination_product_sku(self, destination_product_sku: str) -> 'ProductCopy':
		"""
		Set destination_product_sku.

		:param destination_product_sku: str
		:returns: ProductCopy
		"""

		self.destination_product_sku = destination_product_sku
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductCopy':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductCopy':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductCopy(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.source_product_id is not None:
			data['Source_Product_ID'] = self.source_product_id
		elif self.source_product_code is not None:
			data['Source_Product_Code'] = self.source_product_code

		if self.destination_product_code is not None:
			data['Dest_Product_Code'] = self.destination_product_code

		if self.copy_product_rules_id is not None:
			data['CopyProductRules_ID'] = self.copy_product_rules_id
		elif self.copy_product_rules_name is not None:
			data['CopyProductRules_Name'] = self.copy_product_rules_name

		data['Product_Copy_Session_ID'] = self.product_copy_session_id
		if self.copy_product_rules_id is not None:
			data['CopyProductRules_ID'] = self.copy_product_rules_id
		if self.copy_product_rules_name is not None:
			data['CopyProductRules_Name'] = self.copy_product_rules_name
		if self.destination_product_code is not None:
			data['Dest_Product_Code'] = self.destination_product_code
		if self.destination_product_name is not None:
			data['Dest_Product_Name'] = self.destination_product_name
		if self.destination_product_sku is not None:
			data['Dest_Product_SKU'] = self.destination_product_sku
		return data
