"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderItem_Add. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderitem_add
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderItemAdd(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderItemAdd Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.code = None
		self.name = None
		self.sku = None
		self.quantity = None
		self.price = None
		self.weight = None
		self.taxable = None
		self.options = []
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderItem_Add'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

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

	def set_order_id(self, order_id: int) -> 'OrderItemAdd':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderItemAdd
		"""

		self.order_id = order_id
		return self

	def set_code(self, code: str) -> 'OrderItemAdd':
		"""
		Set Code.

		:param code: str
		:returns: OrderItemAdd
		"""

		self.code = code
		return self

	def set_name(self, name: str) -> 'OrderItemAdd':
		"""
		Set Name.

		:param name: str
		:returns: OrderItemAdd
		"""

		self.name = name
		return self

	def set_sku(self, sku: str) -> 'OrderItemAdd':
		"""
		Set Sku.

		:param sku: str
		:returns: OrderItemAdd
		"""

		self.sku = sku
		return self

	def set_quantity(self, quantity: int) -> 'OrderItemAdd':
		"""
		Set Quantity.

		:param quantity: int
		:returns: OrderItemAdd
		"""

		self.quantity = quantity
		return self

	def set_price(self, price: float) -> 'OrderItemAdd':
		"""
		Set Price.

		:param price: float
		:returns: OrderItemAdd
		"""

		self.price = price
		return self

	def set_weight(self, weight: float) -> 'OrderItemAdd':
		"""
		Set Weight.

		:param weight: float
		:returns: OrderItemAdd
		"""

		self.weight = weight
		return self

	def set_taxable(self, taxable: bool) -> 'OrderItemAdd':
		"""
		Set Taxable.

		:param taxable: bool
		:returns: OrderItemAdd
		"""

		self.taxable = taxable
		return self

	def set_options(self, options: list) -> 'OrderItemAdd':
		"""
		Set Options.

		:param options: {OrderItemOption[]}
		:raises Exception:
		:returns: OrderItemAdd
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception("")
		self.options = options
		return self
	
	def add_option(self, option) -> 'OrderItemAdd':
		"""
		Add Options.

		:param option: OrderItemOption 
		:raises Exception:
		:returns: {OrderItemAdd}
		"""

		if isinstance(option, merchantapi.model.OrderItemOption):
			self.options.append(option)
		elif isinstance(option, dict):
			self.options.append(merchantapi.model.OrderItemOption(option))
		else:
			raise Exception('Expected instance of OrderItemOption or dict')
		return self

	def add_options(self, options: list) -> 'OrderItemAdd':
		"""
		Add many OrderItemOption.

		:param options: List of OrderItemOption
		:raises Exception:
		:returns: OrderItemAdd
		"""

		for e in options:
			if not isinstance(e, merchantapi.model.OrderItemOption):
				raise Exception('')
			self.options.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderItemAdd':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderItemAdd':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderItemAdd(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.get_order_id()

		data['Code'] = self.code
		data['Name'] = self.name
		if self.sku is not None:
			data['Sku'] = self.sku
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
