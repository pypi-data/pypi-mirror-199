"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderCustomFields_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordercustomfields_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderCustomFieldsUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderCustomFieldsUpdate Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderCustomFields_Update'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_order_id(self, order_id: int) -> 'OrderCustomFieldsUpdate':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderCustomFieldsUpdate
		"""

		self.order_id = order_id
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'OrderCustomFieldsUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: OrderCustomFieldsUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCustomFieldsUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCustomFieldsUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCustomFieldsUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
