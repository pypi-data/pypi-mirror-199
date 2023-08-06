"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroupCategory_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcategory_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupCategoryUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCategoryUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.category_id = None
		self.edit_category = None
		self.category_code = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = None
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())
			elif price_group.get_name():
				self.set_edit_price_group(price_group.get_name())
			elif price_group.get_name():
				self.set_price_group_name(price_group.get_name())

			self.set_price_group_name(price_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCategory_Update_Assigned'

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

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_category_id(self, category_id: int) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.category_id = category_id
		return self

	def set_edit_category(self, edit_category: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Edit_Category.

		:param edit_category: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.edit_category = edit_category
		return self

	def set_category_code(self, category_code: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Category_Code.

		:param category_code: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.category_code = category_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCategoryUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCategoryUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCategoryUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCategoryUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		if self.category_id is not None:
			data['Category_ID'] = self.category_id
		elif self.edit_category is not None:
			data['Edit_Category'] = self.edit_category
		elif self.category_code is not None:
			data['Category_Code'] = self.category_code

		data['PriceGroup_Name'] = self.price_group_name
		data['Assigned'] = self.assigned
		return data
