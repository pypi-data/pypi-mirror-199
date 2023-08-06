"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderShipment data model.
"""

from merchantapi.abstract import Model

class OrderShipment(Model):
	# ORDER_SHIPMENT_STATUS constants.
	ORDER_SHIPMENT_STATUS_PENDING = 0
	ORDER_SHIPMENT_STATUS_PICKING = 100
	ORDER_SHIPMENT_STATUS_SHIPPED = 200

	def __init__(self, data: dict = None):
		"""
		OrderShipment Constructor

		:param data: dict
		"""

		super().__init__(data)
		from .order import Order
		from .order_item import OrderItem

		if self.has_field('order'):
			value = self.get_field('order')
			if isinstance(value, dict):
				if not isinstance(value, Order):
					self.set_field('order', Order(value))
			else:
				raise Exception('Expected Order or a dict')

		if self.has_field('items'):
			value = self.get_field('items')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItem):
							value[i] = OrderItem(e)
					else:
						raise Exception('Expected list of OrderItem or dict')
			else:
				raise Exception('Expected list of OrderItem or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_batch_id(self) -> int:
		"""
		Get batch_id.

		:returns: int
		"""

		return self.get_field('batch_id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_label_count(self) -> int:
		"""
		Get labelcount.

		:returns: int
		"""

		return self.get_field('labelcount', 0)

	def get_ship_date(self) -> int:
		"""
		Get ship_date.

		:returns: int
		"""

		return self.get_field('ship_date', 0)

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_tracking_link(self) -> str:
		"""
		Get tracklink.

		:returns: string
		"""

		return self.get_field('tracklink')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_order(self):
		"""
		Get order.

		:returns: Order|None
		"""

		return self.get_field('order', None)

	def get_items(self):
		"""
		Get items.

		:returns: List of OrderItem
		"""

		return self.get_field('items', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'order' in ret and isinstance(ret['order'], Order):
			ret['order'] = ret['order'].to_dict()

		if 'items' in ret and isinstance(ret['items'], list):
			for i, e in enumerate(ret['items']):
				if isinstance(e, OrderItem):
					ret['items'][i] = ret['items'][i].to_dict()

		return ret
