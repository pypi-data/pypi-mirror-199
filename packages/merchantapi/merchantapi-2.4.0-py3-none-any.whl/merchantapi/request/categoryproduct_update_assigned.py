"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryproduct_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryProductUpdateAssigned Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.product_sku = None
		self.assigned = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryProduct_Update_Assigned'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

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

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'CategoryProductUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryProductUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_product_id(self, product_id: int) -> 'CategoryProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: CategoryProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'CategoryProductUpdateAssigned':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: CategoryProductUpdateAssigned
		"""

		self.product_sku = product_sku
		return self

	def set_assigned(self, assigned: bool) -> 'CategoryProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CategoryProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryProductUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Assigned'] = self.assigned
		return data
