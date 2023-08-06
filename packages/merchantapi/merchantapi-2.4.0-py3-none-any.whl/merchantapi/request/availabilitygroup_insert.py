"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AvailabilityGroup_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroup_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AvailabilityGroupInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		AvailabilityGroupInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.availability_group_name = None
		self.availability_group_tax_exempt = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AvailabilityGroup_Insert'

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

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupInsert':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupInsert
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_availability_group_tax_exempt(self, availability_group_tax_exempt: bool) -> 'AvailabilityGroupInsert':
		"""
		Set AvailabilityGroup_Tax_Exempt.

		:param availability_group_tax_exempt: bool
		:returns: AvailabilityGroupInsert
		"""

		self.availability_group_tax_exempt = availability_group_tax_exempt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['AvailabilityGroup_Name'] = self.availability_group_name
		if self.availability_group_tax_exempt is not None:
			data['AvailabilityGroup_Tax_Exempt'] = self.availability_group_tax_exempt
		return data
