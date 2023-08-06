"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroupBusinessAccount_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupbusinessaccount_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupBusinessAccountUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupBusinessAccountUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = None
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupBusinessAccount_Update_Assigned'

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> str:
		"""
		Get Edit_BusinessAccount.

		:returns: str
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

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

	def set_business_account_id(self, business_account_id: int) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupBusinessAccountUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupBusinessAccountUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupBusinessAccountUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupBusinessAccountUpdateAssigned(self, http_response, data)

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

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
