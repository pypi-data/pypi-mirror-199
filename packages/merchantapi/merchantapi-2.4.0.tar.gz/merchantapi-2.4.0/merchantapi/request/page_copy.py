"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Page_Copy. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/page_copy
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageCopy(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, page: merchantapi.model.Page = None):
		"""
		PageCopy Constructor.

		:param client: Client
		:param page: Page
		"""

		super().__init__(client)
		self.source_page_id = None
		self.source_edit_page = None
		self.source_page_code = None
		self.copy_page_rules_id = None
		self.copy_page_rules_name = None
		self.destination_page_id = None
		self.destination_edit_page = None
		self.destination_page_code = None
		self.destination_page_create = None
		self.changeset_notes = None
		self.destination_page_name = None
		self.destination_page_layout = None
		if isinstance(page, merchantapi.model.Page):
			if page.get_id():
				self.set_source_page_id(page.get_id())
			elif page.get_code():
				self.set_source_edit_page(page.get_code())
			elif page.get_code():
				self.set_source_page_code(page.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Page_Copy'

	def get_source_page_id(self) -> int:
		"""
		Get Source_Page_ID.

		:returns: int
		"""

		return self.source_page_id

	def get_source_edit_page(self) -> str:
		"""
		Get Source_Edit_Page.

		:returns: str
		"""

		return self.source_edit_page

	def get_source_page_code(self) -> str:
		"""
		Get Source_Page_Code.

		:returns: str
		"""

		return self.source_page_code

	def get_copy_page_rules_id(self) -> int:
		"""
		Get CopyPageRules_ID.

		:returns: int
		"""

		return self.copy_page_rules_id

	def get_copy_page_rules_name(self) -> str:
		"""
		Get CopyPageRules_Name.

		:returns: str
		"""

		return self.copy_page_rules_name

	def get_destination_page_id(self) -> int:
		"""
		Get destination_page_id.

		:returns: int
		"""

		return self.destination_page_id

	def get_destination_edit_page(self) -> str:
		"""
		Get destination_edit_page.

		:returns: str
		"""

		return self.destination_edit_page

	def get_destination_page_code(self) -> str:
		"""
		Get destination_page_code.

		:returns: str
		"""

		return self.destination_page_code

	def get_destination_page_create(self) -> bool:
		"""
		Get destination_page_create.

		:returns: bool
		"""

		return self.destination_page_create

	def get_changeset_notes(self) -> str:
		"""
		Get Changeset_Notes.

		:returns: str
		"""

		return self.changeset_notes

	def get_destination_page_name(self) -> str:
		"""
		Get destination_page_name.

		:returns: str
		"""

		return self.destination_page_name

	def get_destination_page_layout(self) -> bool:
		"""
		Get destination_page_layout.

		:returns: bool
		"""

		return self.destination_page_layout

	def set_source_page_id(self, source_page_id: int) -> 'PageCopy':
		"""
		Set Source_Page_ID.

		:param source_page_id: int
		:returns: PageCopy
		"""

		self.source_page_id = source_page_id
		return self

	def set_source_edit_page(self, source_edit_page: str) -> 'PageCopy':
		"""
		Set Source_Edit_Page.

		:param source_edit_page: str
		:returns: PageCopy
		"""

		self.source_edit_page = source_edit_page
		return self

	def set_source_page_code(self, source_page_code: str) -> 'PageCopy':
		"""
		Set Source_Page_Code.

		:param source_page_code: str
		:returns: PageCopy
		"""

		self.source_page_code = source_page_code
		return self

	def set_copy_page_rules_id(self, copy_page_rules_id: int) -> 'PageCopy':
		"""
		Set CopyPageRules_ID.

		:param copy_page_rules_id: int
		:returns: PageCopy
		"""

		self.copy_page_rules_id = copy_page_rules_id
		return self

	def set_copy_page_rules_name(self, copy_page_rules_name: str) -> 'PageCopy':
		"""
		Set CopyPageRules_Name.

		:param copy_page_rules_name: str
		:returns: PageCopy
		"""

		self.copy_page_rules_name = copy_page_rules_name
		return self

	def set_destination_page_id(self, destination_page_id: int) -> 'PageCopy':
		"""
		Set destination_page_id.

		:param destination_page_id: int
		:returns: PageCopy
		"""

		self.destination_page_id = destination_page_id
		return self

	def set_destination_edit_page(self, destination_edit_page: str) -> 'PageCopy':
		"""
		Set destination_edit_page.

		:param destination_edit_page: str
		:returns: PageCopy
		"""

		self.destination_edit_page = destination_edit_page
		return self

	def set_destination_page_code(self, destination_page_code: str) -> 'PageCopy':
		"""
		Set destination_page_code.

		:param destination_page_code: str
		:returns: PageCopy
		"""

		self.destination_page_code = destination_page_code
		return self

	def set_destination_page_create(self, destination_page_create: bool) -> 'PageCopy':
		"""
		Set destination_page_create.

		:param destination_page_create: bool
		:returns: PageCopy
		"""

		self.destination_page_create = destination_page_create
		return self

	def set_destination_page_name(self, destination_page_name: str) -> 'PageCopy':
		"""
		Set destination_page_name.

		:param destination_page_name: str
		:returns: PageCopy
		"""

		self.destination_page_name = destination_page_name
		return self

	def set_destination_page_layout(self, destination_page_layout: bool) -> 'PageCopy':
		"""
		Set destination_page_layout.

		:param destination_page_layout: bool
		:returns: PageCopy
		"""

		self.destination_page_layout = destination_page_layout
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageCopy':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageCopy':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageCopy(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.source_page_id is not None:
			data['Source_Page_ID'] = self.source_page_id
		elif self.source_edit_page is not None:
			data['Source_Edit_Page'] = self.source_edit_page
		elif self.source_page_code is not None:
			data['Source_Page_Code'] = self.source_page_code

		if self.destination_page_id is not None:
			data['Dest_Page_ID'] = self.destination_page_id
		elif self.destination_edit_page is not None:
			data['Dest_Edit_Page'] = self.destination_edit_page

		if self.copy_page_rules_id is not None:
			data['CopyPageRules_ID'] = self.copy_page_rules_id
		elif self.copy_page_rules_name is not None:
			data['CopyPageRules_Name'] = self.copy_page_rules_name

		data['Dest_Page_Code'] = self.destination_page_code
		if self.destination_page_create is not None:
			data['Dest_Page_Create'] = self.destination_page_create
		if self.changeset_notes is not None:
			data['Changeset_Notes'] = self.changeset_notes
		data['Dest_Page_Name'] = self.destination_page_name
		if self.destination_page_layout is not None:
			data['Dest_Page_Layout'] = self.destination_page_layout
		return data
