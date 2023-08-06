"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ChildCategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/childcategorylist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import CategoryListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ChildCategoryListLoadQuery(CategoryListLoadQuery):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		ChildCategoryListLoadQuery Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.parent_category_id = None
		self.parent_category_code = None
		self.edit_parent_category = None
		self.assigned = None
		self.unassigned = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_parent_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_parent_category(category.get_code())
			elif category.get_code():
				self.set_parent_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChildCategoryList_Load_Query'

	def get_parent_category_id(self) -> int:
		"""
		Get ParentCategory_ID.

		:returns: int
		"""

		return self.parent_category_id

	def get_parent_category_code(self) -> str:
		"""
		Get ParentCategory_Code.

		:returns: str
		"""

		return self.parent_category_code

	def get_edit_parent_category(self) -> str:
		"""
		Get Edit_ParentCategory.

		:returns: str
		"""

		return self.edit_parent_category

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

	def set_parent_category_id(self, parent_category_id: int) -> 'ChildCategoryListLoadQuery':
		"""
		Set ParentCategory_ID.

		:param parent_category_id: int
		:returns: ChildCategoryListLoadQuery
		"""

		self.parent_category_id = parent_category_id
		return self

	def set_parent_category_code(self, parent_category_code: str) -> 'ChildCategoryListLoadQuery':
		"""
		Set ParentCategory_Code.

		:param parent_category_code: str
		:returns: ChildCategoryListLoadQuery
		"""

		self.parent_category_code = parent_category_code
		return self

	def set_edit_parent_category(self, edit_parent_category: str) -> 'ChildCategoryListLoadQuery':
		"""
		Set Edit_ParentCategory.

		:param edit_parent_category: str
		:returns: ChildCategoryListLoadQuery
		"""

		self.edit_parent_category = edit_parent_category
		return self

	def set_assigned(self, assigned: bool) -> 'ChildCategoryListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: ChildCategoryListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'ChildCategoryListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: ChildCategoryListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChildCategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChildCategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChildCategoryListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.parent_category_id is not None:
			data['ParentCategory_ID'] = self.parent_category_id
		elif self.parent_category_code is not None:
			data['ParentCategory_Code'] = self.parent_category_code
		elif self.edit_parent_category is not None:
			data['Edit_ParentCategory'] = self.edit_parent_category

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
