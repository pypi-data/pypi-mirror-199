"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryurilist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryURIListLoadQuery Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_edit_category(category.get_code())
			elif category.get_code():
				self.set_category_code(category.get_code())

			self.set_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURIList_Load_Query'

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

	def set_category_id(self, category_id: int) -> 'CategoryURIListLoadQuery':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryURIListLoadQuery
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryURIListLoadQuery':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryURIListLoadQuery
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'CategoryURIListLoadQuery':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryURIListLoadQuery
		"""

		self.category_code = category_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIListLoadQuery(self, http_response, data)

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

		data['Category_Code'] = self.category_code
		return data
