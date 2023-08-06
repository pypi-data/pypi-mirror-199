"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PageURI_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pageuri_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageURIInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, page: merchantapi.model.Page = None):
		"""
		PageURIInsert Constructor.

		:param client: Client
		:param page: Page
		"""

		super().__init__(client)
		self.uri = None
		self.status = None
		self.canonical = None
		self.page_id = None
		self.page_code = None
		self.edit_page = None
		if isinstance(page, merchantapi.model.Page):
			if page.get_id():
				self.set_page_id(page.get_id())
			elif page.get_code():
				self.set_page_code(page.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageURI_Insert'

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

	def get_page_id(self) -> int:
		"""
		Get Page_ID.

		:returns: int
		"""

		return self.page_id

	def get_page_code(self) -> str:
		"""
		Get Page_Code.

		:returns: str
		"""

		return self.page_code

	def get_edit_page(self) -> str:
		"""
		Get Edit_Page.

		:returns: str
		"""

		return self.edit_page

	def set_uri(self, uri: str) -> 'PageURIInsert':
		"""
		Set URI.

		:param uri: str
		:returns: PageURIInsert
		"""

		self.uri = uri
		return self

	def set_status(self, status: int) -> 'PageURIInsert':
		"""
		Set Status.

		:param status: int
		:returns: PageURIInsert
		"""

		self.status = status
		return self

	def set_canonical(self, canonical: bool) -> 'PageURIInsert':
		"""
		Set Canonical.

		:param canonical: bool
		:returns: PageURIInsert
		"""

		self.canonical = canonical
		return self

	def set_page_id(self, page_id: int) -> 'PageURIInsert':
		"""
		Set Page_ID.

		:param page_id: int
		:returns: PageURIInsert
		"""

		self.page_id = page_id
		return self

	def set_page_code(self, page_code: str) -> 'PageURIInsert':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageURIInsert
		"""

		self.page_code = page_code
		return self

	def set_edit_page(self, edit_page: str) -> 'PageURIInsert':
		"""
		Set Edit_Page.

		:param edit_page: str
		:returns: PageURIInsert
		"""

		self.edit_page = edit_page
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageURIInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageURIInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageURIInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.page_id is not None:
			data['Page_ID'] = self.page_id
		elif self.page_code is not None:
			data['Page_Code'] = self.page_code
		elif self.edit_page is not None:
			data['Edit_Page'] = self.edit_page

		if self.uri is not None:
			data['URI'] = self.uri
		if self.status is not None:
			data['Status'] = self.status
		if self.canonical is not None:
			data['Canonical'] = self.canonical
		return data
