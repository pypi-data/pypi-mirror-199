"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request RelatedProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/relatedproduct_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class RelatedProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		RelatedProductUpdateAssigned Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.related_product_id = None
		self.related_product_code = None
		self.edit_related_product = None
		self.assigned = None
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

		return 'RelatedProduct_Update_Assigned'

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

	def get_related_product_id(self) -> int:
		"""
		Get RelatedProduct_ID.

		:returns: int
		"""

		return self.related_product_id

	def get_related_product_code(self) -> str:
		"""
		Get RelatedProduct_Code.

		:returns: str
		"""

		return self.related_product_code

	def get_edit_related_product(self) -> str:
		"""
		Get Edit_RelatedProduct.

		:returns: str
		"""

		return self.edit_related_product

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_product_id(self, product_id: int) -> 'RelatedProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: RelatedProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_related_product_id(self, related_product_id: int) -> 'RelatedProductUpdateAssigned':
		"""
		Set RelatedProduct_ID.

		:param related_product_id: int
		:returns: RelatedProductUpdateAssigned
		"""

		self.related_product_id = related_product_id
		return self

	def set_related_product_code(self, related_product_code: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set RelatedProduct_Code.

		:param related_product_code: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.related_product_code = related_product_code
		return self

	def set_edit_related_product(self, edit_related_product: str) -> 'RelatedProductUpdateAssigned':
		"""
		Set Edit_RelatedProduct.

		:param edit_related_product: str
		:returns: RelatedProductUpdateAssigned
		"""

		self.edit_related_product = edit_related_product
		return self

	def set_assigned(self, assigned: bool) -> 'RelatedProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: RelatedProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.RelatedProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'RelatedProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.RelatedProductUpdateAssigned(self, http_response, data)

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

		if self.related_product_id is not None:
			data['RelatedProduct_ID'] = self.related_product_id
		elif self.related_product_code is not None:
			data['RelatedProduct_Code'] = self.related_product_code
		elif self.edit_related_product is not None:
			data['Edit_RelatedProduct'] = self.edit_related_product

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
