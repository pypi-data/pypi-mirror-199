"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PageURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageurilist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None):
		"""
		PageURIListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.page_id = None
		self.edit_page = None
		self.page_code = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURIList_Load_Query'

	def get_page_id(self) -> int:
		"""
		Get Page_ID.

		:returns: int
		"""

		return self.page_id

	def get_edit_page(self) -> str:
		"""
		Get Edit_Page.

		:returns: str
		"""

		return self.edit_page

	def get_page_code(self) -> str:
		"""
		Get Page_Code.

		:returns: str
		"""

		return self.page_code

	def set_page_id(self, page_id: int) -> 'PageURIListLoadQuery':
		"""
		Set Page_ID.

		:param page_id: int
		:returns: PageURIListLoadQuery
		"""

		self.page_id = page_id
		return self

	def set_edit_page(self, edit_page: str) -> 'PageURIListLoadQuery':
		"""
		Set Edit_Page.

		:param edit_page: str
		:returns: PageURIListLoadQuery
		"""

		self.edit_page = edit_page
		return self

	def set_page_code(self, page_code: str) -> 'PageURIListLoadQuery':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageURIListLoadQuery
		"""

		self.page_code = page_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.page_id is not None:
			data['Page_ID'] = self.page_id
		elif self.edit_page is not None:
			data['Edit_Page'] = self.edit_page
		elif self.page_code is not None:
			data['Page_Code'] = self.page_code

		data['Page_Code'] = self.page_code
		return data
