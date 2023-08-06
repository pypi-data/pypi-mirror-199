"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroupQualifyingProduct_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroupqualifyingproduct_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupQualifyingProductUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupQualifyingProductUpdateAssigned Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.assigned = None
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_product_id(price_group.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupQualifyingProduct_Update_Assigned'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

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

	def set_product_id(self, product_id: int) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.product_code = product_code
		return self

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.price_group_name = price_group_name
		return self

	def set_assigned(self, assigned: bool) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: PriceGroupQualifyingProductUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupQualifyingProductUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupQualifyingProductUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupQualifyingProductUpdateAssigned(self, http_response, data)

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

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		data['PriceGroup_Name'] = self.price_group_name
		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
