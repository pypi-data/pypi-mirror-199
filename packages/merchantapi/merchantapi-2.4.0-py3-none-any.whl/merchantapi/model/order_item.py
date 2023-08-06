"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderItem data model.
"""

from merchantapi.abstract import Model
from .order_shipment import OrderShipment
from .order_item_discount import OrderItemDiscount
from .order_item_option import OrderItemOption
from .order_item_subscription import OrderItemSubscription

class OrderItem(Model):
	# ORDER_ITEM_STATUS constants.
	ORDER_ITEM_STATUS_PENDING = 0
	ORDER_ITEM_STATUS_PROCESSING = 100
	ORDER_ITEM_STATUS_SHIPPED = 200
	ORDER_ITEM_STATUS_PARTIALLY_SHIPPED = 201
	ORDER_ITEM_STATUS_GIFT_CERT_NOT_REDEEMED = 210
	ORDER_ITEM_STATUS_GIFT_CERT_REDEEMED = 211
	ORDER_ITEM_STATUS_DIGITAL_NOT_DOWNLOADED = 220
	ORDER_ITEM_STATUS_DIGITAL_DOWNLOADED = 221
	ORDER_ITEM_STATUS_CANCELLED = 300
	ORDER_ITEM_STATUS_BACKORDERED = 400
	ORDER_ITEM_STATUS_RMA_ISSUED = 500
	ORDER_ITEM_STATUS_RETURNED = 600

	def __init__(self, data: dict = None):
		"""
		OrderItem Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('shipment'):
			value = self.get_field('shipment')
			if isinstance(value, dict):
				if not isinstance(value, OrderShipment):
					self.set_field('shipment', OrderShipment(value))
			else:
				raise Exception('Expected OrderShipment or a dict')

		if self.has_field('discounts'):
			value = self.get_field('discounts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItemDiscount):
							value[i] = OrderItemDiscount(e)
					else:
						raise Exception('Expected list of OrderItemDiscount or dict')
			else:
				raise Exception('Expected list of OrderItemDiscount or dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItemOption):
							value[i] = OrderItemOption(e)
					else:
						raise Exception('Expected list of OrderItemOption or dict')
			else:
				raise Exception('Expected list of OrderItemOption or dict')

		if self.has_field('subscription'):
			value = self.get_field('subscription')
			if isinstance(value, dict):
				if not isinstance(value, OrderItemSubscription):
					self.set_field('subscription', OrderItemSubscription(value))
			else:
				raise Exception('Expected OrderItemSubscription or a dict')

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_line_id(self) -> int:
		"""
		Get line_id.

		:returns: int
		"""

		return self.get_field('line_id', 0)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_subscription_id(self) -> int:
		"""
		Get subscrp_id.

		:returns: int
		"""

		return self.get_field('subscrp_id', 0)

	def get_subscription_term_id(self) -> int:
		"""
		Get subterm_id.

		:returns: int
		"""

		return self.get_field('subterm_id', 0)

	def get_rma_id(self) -> int:
		"""
		Get rma_id.

		:returns: int
		"""

		return self.get_field('rma_id', 0)

	def get_rma_code(self) -> str:
		"""
		Get rma_code.

		:returns: string
		"""

		return self.get_field('rma_code')

	def get_rma_data_time_issued(self) -> int:
		"""
		Get rma_dt_issued.

		:returns: int
		"""

		return self.get_timestamp_field('rma_dt_issued')

	def get_rma_date_time_received(self) -> int:
		"""
		Get rma_dt_recvd.

		:returns: int
		"""

		return self.get_timestamp_field('rma_dt_recvd')

	def get_date_in_stock(self) -> int:
		"""
		Get dt_instock.

		:returns: int
		"""

		return self.get_timestamp_field('dt_instock')

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_retail(self) -> float:
		"""
		Get retail.

		:returns: float
		"""

		return self.get_field('retail', 0.00)

	def get_base_price(self) -> float:
		"""
		Get base_price.

		:returns: float
		"""

		return self.get_field('base_price', 0.00)

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_tax(self) -> float:
		"""
		Get tax.

		:returns: float
		"""

		return self.get_field('tax', 0.00)

	def get_formatted_tax(self) -> str:
		"""
		Get formatted_tax.

		:returns: string
		"""

		return self.get_field('formatted_tax')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_taxable(self) -> bool:
		"""
		Get taxable.

		:returns: bool
		"""

		return self.get_field('taxable', False)

	def get_upsold(self) -> bool:
		"""
		Get upsold.

		:returns: bool
		"""

		return self.get_field('upsold', False)

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_shipment(self):
		"""
		Get shipment.

		:returns: OrderShipment|None
		"""

		return self.get_field('shipment', None)

	def get_discounts(self):
		"""
		Get discounts.

		:returns: List of OrderItemDiscount
		"""

		return self.get_field('discounts', [])

	def get_options(self):
		"""
		Get options.

		:returns: List of OrderItemOption
		"""

		return self.get_field('options', [])

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_shipment_id(self) -> int:
		"""
		Get shpmnt_id.

		:returns: int
		"""

		return self.get_field('shpmnt_id', 0)

	def get_subscription(self):
		"""
		Get subscription.

		:returns: OrderItemSubscription|None
		"""

		return self.get_field('subscription', None)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def set_code(self, code: str) -> 'OrderItem':
		"""
		Set code.

		:param code: string
		:returns: OrderItem
		"""

		return self.set_field('code', code)

	def set_name(self, name: str) -> 'OrderItem':
		"""
		Set name.

		:param name: string
		:returns: OrderItem
		"""

		return self.set_field('name', name)

	def set_sku(self, sku: str) -> 'OrderItem':
		"""
		Set sku.

		:param sku: string
		:returns: OrderItem
		"""

		return self.set_field('sku', sku)

	def set_price(self, price: float) -> 'OrderItem':
		"""
		Set price.

		:param price: int
		:returns: OrderItem
		"""

		return self.set_field('price', price)

	def set_tax(self, tax: float) -> 'OrderItem':
		"""
		Set tax.

		:param tax: int
		:returns: OrderItem
		"""

		return self.set_field('tax', tax)

	def set_weight(self, weight: float) -> 'OrderItem':
		"""
		Set weight.

		:param weight: int
		:returns: OrderItem
		"""

		return self.set_field('weight', weight)

	def set_taxable(self, taxable: bool) -> 'OrderItem':
		"""
		Set taxable.

		:param taxable: bool
		:returns: OrderItem
		"""

		return self.set_field('taxable', taxable)

	def set_upsold(self, upsold: bool) -> 'OrderItem':
		"""
		Set upsold.

		:param upsold: bool
		:returns: OrderItem
		"""

		return self.set_field('upsold', upsold)

	def set_quantity(self, quantity: int) -> 'OrderItem':
		"""
		Set quantity.

		:param quantity: int
		:returns: OrderItem
		"""

		return self.set_field('quantity', quantity)

	def set_options(self, options: list) -> 'OrderItem':
		"""
		Set options.

		:param options: List of OrderItemOption 
		:raises Exception:
		:returns: OrderItem
		"""

		for i, e in enumerate(options, 0):
			if isinstance(e, OrderItemOption):
				continue
			elif isinstance(e, dict):
				options[i] = OrderItemOption(e)
			else:
				raise Exception('Expected instance of OrderItemOption or dict')
		return self.set_field('options', options)

	def set_tracking_type(self, tracking_type: str) -> 'OrderItem':
		"""
		Set tracktype.

		:param tracking_type: string
		:returns: OrderItem
		"""

		return self.set_field('tracktype', tracking_type)

	def set_tracking_number(self, tracking_number: str) -> 'OrderItem':
		"""
		Set tracknum.

		:param tracking_number: string
		:returns: OrderItem
		"""

		return self.set_field('tracknum', tracking_number)
	
	def add_option(self, option: 'OrderItemOption') -> 'OrderItem':
		"""
		Add a OrderItemOption.
		
		:param option: OrderItemOption
		:returns: OrderItem
		"""

		if 'options' not in self:
			self['options'] = []
		self['options'].append(option)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'shipment' in ret and isinstance(ret['shipment'], OrderShipment):
			ret['shipment'] = ret['shipment'].to_dict()

		if 'discounts' in ret and isinstance(ret['discounts'], list):
			for i, e in enumerate(ret['discounts']):
				if isinstance(e, OrderItemDiscount):
					ret['discounts'][i] = ret['discounts'][i].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, OrderItemOption):
					ret['options'][i] = ret['options'][i].to_dict()

		if 'subscription' in ret and isinstance(ret['subscription'], OrderItemSubscription):
			ret['subscription'] = ret['subscription'].to_dict()

		return ret
