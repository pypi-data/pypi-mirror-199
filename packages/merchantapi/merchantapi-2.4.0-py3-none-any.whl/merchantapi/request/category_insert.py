"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Category_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/category_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		CategoryInsert Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_code = None
		self.category_name = None
		self.category_active = None
		self.category_page_title = None
		self.category_parent_category = None
		self.category_alternate_display_page = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(category, merchantapi.model.Category):
			self.set_category_code(category.get_code())
			self.set_category_name(category.get_name())
			self.set_category_active(category.get_active())
			self.set_category_page_title(category.get_page_title())
			self.set_category_parent_category(category.get_parent_category())
			self.set_category_alternate_display_page(category.get_page_code())

			if category.get_custom_field_values():
				self.set_custom_field_values(category.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Category_Insert'

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: str
		"""

		return self.category_code

	def get_category_name(self) -> str:
		"""
		Get Category_Name.

		:returns: str
		"""

		return self.category_name

	def get_category_active(self) -> bool:
		"""
		Get Category_Active.

		:returns: bool
		"""

		return self.category_active

	def get_category_page_title(self) -> str:
		"""
		Get Category_Page_Title.

		:returns: str
		"""

		return self.category_page_title

	def get_category_parent_category(self) -> str:
		"""
		Get Category_Parent_Category.

		:returns: str
		"""

		return self.category_parent_category

	def get_category_alternate_display_page(self) -> str:
		"""
		Get Category_Alternate_Display_Page.

		:returns: str
		"""

		return self.category_alternate_display_page

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_category_code(self, category_code: str) -> 'CategoryInsert':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: CategoryInsert
		"""

		self.category_code = category_code
		return self

	def set_category_name(self, category_name: str) -> 'CategoryInsert':
		"""
		Set Category_Name.

		:param category_name: str
		:returns: CategoryInsert
		"""

		self.category_name = category_name
		return self

	def set_category_active(self, category_active: bool) -> 'CategoryInsert':
		"""
		Set Category_Active.

		:param category_active: bool
		:returns: CategoryInsert
		"""

		self.category_active = category_active
		return self

	def set_category_page_title(self, category_page_title: str) -> 'CategoryInsert':
		"""
		Set Category_Page_Title.

		:param category_page_title: str
		:returns: CategoryInsert
		"""

		self.category_page_title = category_page_title
		return self

	def set_category_parent_category(self, category_parent_category: str) -> 'CategoryInsert':
		"""
		Set Category_Parent_Category.

		:param category_parent_category: str
		:returns: CategoryInsert
		"""

		self.category_parent_category = category_parent_category
		return self

	def set_category_alternate_display_page(self, category_alternate_display_page: str) -> 'CategoryInsert':
		"""
		Set Category_Alternate_Display_Page.

		:param category_alternate_display_page: str
		:returns: CategoryInsert
		"""

		self.category_alternate_display_page = category_alternate_display_page
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CategoryInsert':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CategoryInsert
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Category_Code'] = self.category_code
		data['Category_Name'] = self.category_name
		if self.category_active is not None:
			data['Category_Active'] = self.category_active
		if self.category_page_title is not None:
			data['Category_Page_Title'] = self.category_page_title
		if self.category_parent_category is not None:
			data['Category_Parent_Category'] = self.category_parent_category
		if self.category_alternate_display_page is not None:
			data['Category_Alternate_Display_Page'] = self.category_alternate_display_page
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
