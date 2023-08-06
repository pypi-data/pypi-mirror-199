"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AvailabilityGroupBusinessAccount_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupbusinessaccount_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AvailabilityGroupBusinessAccountUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupBusinessAccountUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.business_account_id = None
		self.business_account_title = None
		self.assigned = None
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())
			elif availability_group.get_name():
				self.set_edit_availability_group(availability_group.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroupBusinessAccount_Update_Assigned'

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

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_business_account_id(self, business_account_id: int) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_business_account_title(self, business_account_title: str) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupBusinessAccountUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupBusinessAccountUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupBusinessAccountUpdateAssigned(self, http_response, data)

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

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
