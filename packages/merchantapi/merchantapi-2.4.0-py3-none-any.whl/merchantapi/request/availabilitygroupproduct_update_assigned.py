"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AvailabilityGroupProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/availabilitygroupproduct_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AvailabilityGroupProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, availability_group: merchantapi.model.AvailabilityGroup = None):
		"""
		AvailabilityGroupProductUpdateAssigned Constructor.

		:param client: Client
		:param availability_group: AvailabilityGroup
		"""

		super().__init__(client)
		self.availability_group_id = None
		self.edit_availability_group = None
		self.availability_group_name = None
		self.product_id = None
		self.product_code = None
		self.product_sku = None
		self.edit_product = None
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

		return 'AvailabilityGroupProduct_Update_Assigned'

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

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_availability_group_id(self, availability_group_id: int) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set AvailabilityGroup_ID.

		:param availability_group_id: int
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.availability_group_id = availability_group_id
		return self

	def set_edit_availability_group(self, edit_availability_group: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Edit_AvailabilityGroup.

		:param edit_availability_group: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.edit_availability_group = edit_availability_group
		return self

	def set_availability_group_name(self, availability_group_name: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set AvailabilityGroup_Name.

		:param availability_group_name: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.availability_group_name = availability_group_name
		return self

	def set_product_id(self, product_id: int) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.product_sku = product_sku
		return self

	def set_edit_product(self, edit_product: str) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_assigned(self, assigned: bool) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: AvailabilityGroupProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AvailabilityGroupProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AvailabilityGroupProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AvailabilityGroupProductUpdateAssigned(self, http_response, data)

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

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Assigned'] = self.assigned
		return data
