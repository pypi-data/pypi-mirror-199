"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Page_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/page_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		PageInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.page_code = None
		self.page_name = None
		self.page_title = None
		self.page_template = None
		self.page_layout = None
		self.page_secure = None
		self.page_cache = None
		self.changeset_notes = None
		self.page_uri = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Page_Insert'

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

	def get_page_template(self) -> str:
		"""
		Get Page_Template.

		:returns: str
		"""

		return self.page_template

	def get_page_layout(self) -> bool:
		"""
		Get Page_Layout.

		:returns: bool
		"""

		return self.page_layout

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

	def set_page_code(self, page_code: str) -> 'PageInsert':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageInsert
		"""

		self.page_code = page_code
		return self

	def set_page_name(self, page_name: str) -> 'PageInsert':
		"""
		Set Page_Name.

		:param page_name: str
		:returns: PageInsert
		"""

		self.page_name = page_name
		return self

	def set_page_title(self, page_title: str) -> 'PageInsert':
		"""
		Set Page_Title.

		:param page_title: str
		:returns: PageInsert
		"""

		self.page_title = page_title
		return self

	def set_page_template(self, page_template: str) -> 'PageInsert':
		"""
		Set Page_Template.

		:param page_template: str
		:returns: PageInsert
		"""

		self.page_template = page_template
		return self

	def set_page_layout(self, page_layout: bool) -> 'PageInsert':
		"""
		Set Page_Layout.

		:param page_layout: bool
		:returns: PageInsert
		"""

		self.page_layout = page_layout
		return self

	def set_page_secure(self, page_secure: bool) -> 'PageInsert':
		"""
		Set Page_Secure.

		:param page_secure: bool
		:returns: PageInsert
		"""

		self.page_secure = page_secure
		return self

	def set_page_cache(self, page_cache: str) -> 'PageInsert':
		"""
		Set Page_Cache.

		:param page_cache: str
		:returns: PageInsert
		"""

		self.page_cache = page_cache
		return self

	def set_changeset_notes(self, changeset_notes: str) -> 'PageInsert':
		"""
		Set Changeset_Notes.

		:param changeset_notes: str
		:returns: PageInsert
		"""

		self.changeset_notes = changeset_notes
		return self

	def set_page_uri(self, page_uri: str) -> 'PageInsert':
		"""
		Set Page_URI.

		:param page_uri: str
		:returns: PageInsert
		"""

		self.page_uri = page_uri
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'PageInsert':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: PageInsert
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Page_Code'] = self.page_code
		data['Page_Name'] = self.page_name
		if self.page_title is not None:
			data['Page_Title'] = self.page_title
		if self.page_template is not None:
			data['Page_Template'] = self.page_template
		if self.page_layout is not None:
			data['Page_Layout'] = self.page_layout
		if self.page_secure is not None:
			data['Page_Secure'] = self.page_secure
		if self.page_cache is not None:
			data['Page_Cache'] = self.page_cache
		if self.changeset_notes is not None:
			data['Changeset_Notes'] = self.changeset_notes
		if self.page_uri is not None:
			data['Page_URI'] = self.page_uri
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
