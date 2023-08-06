"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryProductList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryproductlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import ProductListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryProductListLoadQuery(ProductListLoadQuery):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryProductListLoadQuery Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.category_code = None
		self.edit_category = None
		self.assigned = None
		self.unassigned = None
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

		return 'CategoryProductList_Load_Query'

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.category_id

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: str
		"""

		return self.edit_category

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_category_id(self, category_id: int) -> 'CategoryProductListLoadQuery':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryProductListLoadQuery
		"""

		self.category_id = category_id
		return self

	def set_category_code(self, category_code: str) -> 'CategoryProductListLoadQuery':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryProductListLoadQuery
		"""

		self.category_code = category_code
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryProductListLoadQuery':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryProductListLoadQuery
		"""

		self.edit_category = edit_category
		return self

	def set_assigned(self, assigned: bool) -> 'CategoryProductListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CategoryProductListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CategoryProductListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CategoryProductListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryProductListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryProductListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryProductListLoadQuery(self, http_response, data)

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

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
