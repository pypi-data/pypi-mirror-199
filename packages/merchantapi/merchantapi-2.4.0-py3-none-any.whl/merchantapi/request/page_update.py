"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Page_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/page_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, page: merchantapi.model.Page = None):
		"""
		PageUpdate Constructor.

		:param client: Client
		:param page: Page
		"""

		super().__init__(client)
		self.page_id = None
		self.edit_page = None
		self.page_code = None
		self.page_name = None
		self.page_title = None
		self.page_secure = None
		self.page_cache = None
		self.changeset_notes = None
		self.page_uri = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(page, merchantapi.model.Page):
			if page.get_id():
				self.set_page_id(page.get_id())
			elif page.get_code():
				self.set_edit_page(page.get_code())

			self.set_page_code(page.get_code())

			if page.get_custom_field_values():
				self.set_custom_field_values(page.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Page_Update'

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

	def get_page_name(self) -> str:
		"""
		Get Page_Name.

		:returns: str
		"""

		return self.page_name

	def get_page_title(self) -> str:
		"""
		Get Page_Title.

		:returns: str
		"""

		return self.page_title

	def get_page_secure(self) -> bool:
		"""
		Get Page_Secure.

		:returns: bool
		"""

		return self.page_secure

	def get_page_cache(self) -> str:
		"""
		Get Page_Cache.

		:returns: str
		"""

		return self.page_cache

	def get_changeset_notes(self) -> str:
		"""
		Get Changeset_Notes.

		:returns: str
		"""

		return self.changeset_notes

	def get_page_uri(self) -> str:
		"""
		Get Page_URI.

		:returns: str
		"""

		return self.page_uri

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_page_id(self, page_id: int) -> 'PageUpdate':
		"""
		Set Page_ID.

		:param page_id: int
		:returns: PageUpdate
		"""

		self.page_id = page_id
		return self

	def set_edit_page(self, edit_page: str) -> 'PageUpdate':
		"""
		Set Edit_Page.

		:param edit_page: str
		:returns: PageUpdate
		"""

		self.edit_page = edit_page
		return self

	def set_page_code(self, page_code: str) -> 'PageUpdate':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageUpdate
		"""

		self.page_code = page_code
		return self

	def set_page_name(self, page_name: str) -> 'PageUpdate':
		"""
		Set Page_Name.

		:param page_name: str
		:returns: PageUpdate
		"""

		self.page_name = page_name
		return self

	def set_page_title(self, page_title: str) -> 'PageUpdate':
		"""
		Set Page_Title.

		:param page_title: str
		:returns: PageUpdate
		"""

		self.page_title = page_title
		return self

	def set_page_secure(self, page_secure: bool) -> 'PageUpdate':
		"""
		Set Page_Secure.

		:param page_secure: bool
		:returns: PageUpdate
		"""

		self.page_secure = page_secure
		return self

	def set_page_cache(self, page_cache: str) -> 'PageUpdate':
		"""
		Set Page_Cache.

		:param page_cache: str
		:returns: PageUpdate
		"""

		self.page_cache = page_cache
		return self

	def set_changeset_notes(self, changeset_notes: str) -> 'PageUpdate':
		"""
		Set Changeset_Notes.

		:param changeset_notes: str
		:returns: PageUpdate
		"""

		self.changeset_notes = changeset_notes
		return self

	def set_page_uri(self, page_uri: str) -> 'PageUpdate':
		"""
		Set Page_URI.

		:param page_uri: str
		:returns: PageUpdate
		"""

		self.page_uri = page_uri
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'PageUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: PageUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageUpdate(self, http_response, data)

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

		if self.page_code is not None:
			data['Page_Code'] = self.page_code
		data['Page_Name'] = self.page_name
		if self.page_title is not None:
			data['Page_Title'] = self.page_title
		if self.page_secure is not None:
			data['Page_Secure'] = self.page_secure
		data['Page_Cache'] = self.page_cache
		if self.changeset_notes is not None:
			data['Changeset_Notes'] = self.changeset_notes
		if self.page_uri is not None:
			data['Page_URI'] = self.page_uri
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
