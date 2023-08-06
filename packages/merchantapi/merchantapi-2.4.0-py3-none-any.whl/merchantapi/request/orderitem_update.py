"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderItem_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitem_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderItemUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_item: merchantapi.model.OrderItem = None):
		"""
		OrderItemUpdate Constructor.

		:param client: Client
		:param order_item: OrderItem
		"""

		super().__init__(client)
		self.order_id = None
		self.line_id = None
		self.code = None
		self.name = None
		self.sku = None
		self.quantity = None
		self.price = None
		self.weight = None
		self.taxable = None
		self.options = []
		if isinstance(order_item, merchantapi.model.OrderItem):
			self.set_order_id(order_item.get_order_id())
			self.set_line_id(order_item.get_line_id())
			self.set_code(order_item.get_code())
			self.set_name(order_item.get_name())
			self.set_sku(order_item.get_sku())
			self.set_quantity(order_item.get_quantity())
			self.set_price(order_item.get_price())
			self.set_weight(order_item.get_weight())
			self.set_taxable(order_item.get_taxable())

			if len(order_item.get_options()):
				self.options = order_item.get_options()

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItem_Update'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_line_id(self) -> int:
		"""
		Get Line_ID.

		:returns: int
		"""

		return self.line_id

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_sku(self) -> str:
		"""
		Get Sku.

		:returns: str
		"""

		return self.sku

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def get_price(self) -> float:
		"""
		Get Price.

		:returns: float
		"""

		return self.price

	def get_weight(self) -> float:
		"""
		Get Weight.

		:returns: float
		"""

		return self.weight

	def get_taxable(self) -> bool:
		"""
		Get Taxable.

		:returns: bool
		"""

		return self.taxable

	def get_options(self) -> list:
		"""
		Get Options.

		:returns: List of OrderItemOption
		"""

		return self.options

	def set_order_id(self, order_id: int) -> 'OrderItemUpdate':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemUpdate
		"""

		self.order_id = order_id
		return self

	def set_line_id(self, line_id: int) -> 'OrderItemUpdate':
		"""
		Set Line_ID.

		:param line_id: int
		:returns: OrderItemUpdate
		"""

		self.line_id = line_id
		return self

	def set_code(self, code: str) -> 'OrderItemUpdate':
		"""
		Set Code.

		:param code: str
		:returns: OrderItemUpdate
		"""

		self.code = code
		return self

	def set_name(self, name: str) -> 'OrderItemUpdate':
		"""
		Set Name.

		:param name: str
		:returns: OrderItemUpdate
		"""

		self.name = name
		return self

	def set_sku(self, sku: str) -> 'OrderItemUpdate':
		"""
		Set Sku.

		:param sku: str
		:returns: OrderItemUpdate
		"""

		self.sku = sku
		return self

	def set_quantity(self, quantity: int) -> 'OrderItemUpdate':
		"""
		Set Quantity.

		:param quantity: int
		:returns: OrderItemUpdate
		"""

		self.quantity = quantity
		return self

	def set_price(self, price: float) -> 'OrderItemUpdate':
		"""
		Set Price.

		:param price: float
		:returns: OrderItemUpdate
		"""

		self.price = price
		return self

	def set_weight(self, weight: float) -> 'OrderItemUpdate':
		"""
		Set Weight.

		:param weight: float
		:returns: OrderItemUpdate
		"""

		self.weight = weight
		return self

	def set_taxable(self, taxable: bool) -> 'OrderItemUpdate':
		"""
		Set Taxable.

		:param taxable: bool
		:returns: OrderItemUpdate
		"""

		self.taxable = taxable
		return self

	def set_options(self, options: list) -> 'OrderItemUpdate':
		"""
		Set Options.

		:param options: {OrderItemOption[]}
		:raises Exception:
		:returns: OrderItemUpdate
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception("")
		self.options = options
		return self
	
	def add_option(self, option) -> 'OrderItemUpdate':
		"""
		Add Options.

		:param option: OrderItemOption 
		:raises Exception:
		:returns: {OrderItemUpdate}
		"""

		if isinstance(option, merchantapi.model.OrderItemOption):
			self.options.append(option)
		elif isinstance(option, dict):
			self.options.append(merchantapi.model.OrderItemOption(option))
		else:
			raise Exception('Expected instance of OrderItemOption or dict')
		return self

	def add_options(self, options: list) -> 'OrderItemUpdate':
		"""
		Add many OrderItemOption.

		:param options: List of OrderItemOption
		:raises Exception:
		:returns: OrderItemUpdate
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception('')
			self.options.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Line_ID'] = self.get_line_id()

		if self.code is not None:
			data['Code'] = self.code
		if self.name is not None:
			data['Name'] = self.name
		if self.sku is not None:
			data['Sku'] = self.sku
		if self.quantity is not None:
			data['Quantity'] = self.quantity
		if self.price is not None:
			data['Price'] = self.price
		if self.weight is not None:
			data['Weight'] = self.weight
		if self.taxable is not None:
			data['Taxable'] = self.taxable
		if len(self.options):
			data['Options'] = []

			for f in self.options:
				data['Options'].append(f.to_dict())
		return data
