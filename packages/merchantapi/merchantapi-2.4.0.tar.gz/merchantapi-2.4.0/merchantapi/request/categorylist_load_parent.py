"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryList_Load_Parent. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categorylist_load_parent
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryListLoadParent(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryListLoadParent Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.parent_id = None
		if isinstance(category, merchantapi.model.Category):
			self.set_parent_id(category.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryList_Load_Parent'

	def get_parent_id(self) -> int:
		"""
		Get Parent_ID.

		:returns: int
		"""

		return self.parent_id

	def set_parent_id(self, parent_id: int) -> 'CategoryListLoadParent':
		"""
		Set Parent_ID.

		:param parent_id: int
		:returns: CategoryListLoadParent
		"""

		self.parent_id = parent_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryListLoadParent':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryListLoadParent':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryListLoadParent(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Parent_ID'] = self.get_parent_id()

		return data
