"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AvailabilityGroupCategory_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupcategory_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AvailabilityGroupCategoryUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, category: merchantapi.model.Category = None):
		"""
		AvailabilityGroupCategoryUpdateAssigned Constructor.

		:param client: Client
		:param category: Category
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.assigned = None
		if isinstance(category, merchantapi.model.Category):
			if category.get_id():
				self.set_category_id(category.get_id())

			self.set_category_code(category.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupCategory_Update_Assigned'

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

	def get_availability_group_id(self) -> int:
		"""
		Get AvailabilityGroup_ID.

		:returns: int
		"""

		return self.availability_group_id

	def get_edit_availability_group(self) -> str:
		"""
		Get Edit_AvailabilityGroup.

		:returns: str
		"""

		return self.edit_availability_group

	def get_availability_group_name(self) -> str:
		"""
		Get AvailabilityGroup_Name.

		:returns: str
		"""

		return self.availability_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupCategoryUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupCategoryUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupCategoryUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupCategoryUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.availability_group_id is not None:
			data['AvailabilityGroup_ID'] = self.availability_group_id
		elif self.edit_availability_group is not None:
			data['Edit_AvailabilityGroup'] = self.edit_availability_group
		elif self.availability_group_name is not None:
			data['AvailabilityGroup_Name'] = self.availability_group_name

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		data['Category_Code'] = self.category_code
		data['AvailabilityGroup_Name'] = self.availability_group_name
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
