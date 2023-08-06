"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroupCategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupcategorylist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import CategoryListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupCategoryListLoadQuery(CategoryListLoadQuery):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupCategoryListLoadQuery Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = None
		self.unassigned = None
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupCategoryList_Load_Query'

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

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: PriceGroupCategoryListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupCategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupCategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupCategoryListLoadQuery(self, http_response, data)

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

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
