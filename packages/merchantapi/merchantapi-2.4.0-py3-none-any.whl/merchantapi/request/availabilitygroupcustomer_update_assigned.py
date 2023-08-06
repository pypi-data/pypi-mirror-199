"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AvailabilityGroupCustomer_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupcustomer_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AvailabilityGroupCustomerUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupCustomerUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
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

		return 'AvailabilityGroupCustomer_Update_Assigned'

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

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_customer_id(self, customer_id: int) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.customer_login = customer_login
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupCustomerUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupCustomerUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupCustomerUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupCustomerUpdateAssigned(self, http_response, data)

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

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
