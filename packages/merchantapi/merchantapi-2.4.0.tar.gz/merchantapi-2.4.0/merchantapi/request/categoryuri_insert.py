"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categoryuri_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryURIInsert Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.uri = None
		self.status = None
		self.canonical = None
		self.category_id = None
		self.category_code = None
		self.edit_category = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())
			elif category.get_code():
				self.set_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryURI_Insert'

	def get_uri(self) -> str:
		"""
		Get URI.

		:returns: str
		"""

		return self.uri

	def get_status(self) -> int:
		"""
		Get Status.

		:returns: int
		"""

		return self.status

	def get_canonical(self) -> bool:
		"""
		Get Canonical.

		:returns: bool
		"""

		return self.canonical

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

	def set_uri(self, uri: str) -> 'CategoryURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: CategoryURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'CategoryURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: CategoryURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'CategoryURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: CategoryURIInsert
		"""

		self.canonical = canonical
		return self

	def set_category_id(self, category_id: int) -> 'CategoryURIInsert':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: CategoryURIInsert
		"""

		self.category_id = category_id
		return self

	def set_category_code(self, category_code: str) -> 'CategoryURIInsert':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryURIInsert
		"""

		self.category_code = category_code
		return self

	def set_edit_category(self, edit_category: str) -> 'CategoryURIInsert':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: CategoryURIInsert
		"""

		self.edit_category = edit_category
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data
