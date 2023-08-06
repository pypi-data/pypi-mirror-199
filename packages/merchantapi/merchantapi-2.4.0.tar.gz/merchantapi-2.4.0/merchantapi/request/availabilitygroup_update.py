"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AvailabilityGroup_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroup_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AvailabilityGroupUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupUpdate Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.availability_group_tax_exempt = None
		if isinstance(availability_group, merchantapi.model.AvailabilityGroup):
			if availability_group.get_id():
				self.set_availability_group_id(availability_group.get_id())

			self.set_availability_group_tax_exempt(availability_group.get_tax_exempt())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroup_Update'

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

	def get_availability_group_tax_exempt(self) -> bool:
		"""
		Get AvailabilityGroup_Tax_Exempt.

		:returns: bool
		"""

		return self.availability_group_tax_exempt

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupUpdate':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupUpdate
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupUpdate':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupUpdate
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupUpdate':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupUpdate
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_availability_group_tax_exempt(self, availability_group_tax_exempt: bool) -> 'AvailabilityGroupUpdate':
		"""
		Set AvailabilityGroup_Tax_Exempt.

		:param availability_group_tax_exempt: bool
		:returns: AvailabilityGroupUpdate
		"""

		self.availability_group_tax_exempt = availability_group_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupUpdate(self, http_response, data)

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

		data['AvailabilityGroup_Name'] = self.availability_group_name
		if self.availability_group_tax_exempt is not None:
			data['AvailabilityGroup_Tax_Exempt'] = self.availability_group_tax_exempt
		return data
