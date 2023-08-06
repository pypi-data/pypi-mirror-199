"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Order_Authorize. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_authorize
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderAuthorize(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderAuthorize Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.module_id = None
		self.module_data = None
		self.amount = None
		self.module_fields = {}
		if isinstance(order, merchantapi.model.Order):
			if order.get_id():
				self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Authorize'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_module_id(self) -> int:
		"""
		Get Module_ID.

		:returns: int
		"""

		return self.module_id

	def get_module_data(self) -> str:
		"""
		Get Module_Data.

		:returns: str
		"""

		return self.module_data

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_order_id(self, order_id: int) -> 'OrderAuthorize':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderAuthorize
		"""

		self.order_id = order_id
		return self

	def set_module_id(self, module_id: int) -> 'OrderAuthorize':
		"""
		Set Module_ID.

		:param module_id: int
		:returns: OrderAuthorize
		"""

		self.module_id = module_id
		return self

	def set_module_data(self, module_data: str) -> 'OrderAuthorize':
		"""
		Set Module_Data.

		:param module_data: str
		:returns: OrderAuthorize
		"""

		self.module_data = module_data
		return self

	def set_amount(self, amount: float) -> 'OrderAuthorize':
		"""
		Set Amount.

		:param amount: float
		:returns: OrderAuthorize
		"""

		self.amount = amount
		return self

	def set_module_fields(self, module_fields) -> 'OrderAuthorize':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: OrderAuthorize
		"""

		self.module_fields = module_fields
		return self

	def set_module_field(self, field: str, value) -> 'OrderAuthorize':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {OrderAuthorize}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderAuthorize':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderAuthorize':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderAuthorize(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.module_id is not None:
			data['Module_ID'] = self.module_id
		if self.module_data is not None:
			data['Module_Data'] = self.module_data
		data['Amount'] = self.amount
		return data
