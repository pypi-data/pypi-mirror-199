"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderTotalAndItem data model.
"""

from .order_total import OrderTotal
from .order_item import OrderItem

class OrderTotalAndItem(OrderTotal):
	def __init__(self, data: dict = None):
		"""
		OrderTotalAndItem Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('orderitem'):
			value = self.get_field('orderitem')
			if isinstance(value, dict):
				if not isinstance(value, OrderItem):
					self.set_field('orderitem', OrderItem(value))
			else:
				raise Exception('Expected OrderItem or a dict')

	def get_order_item(self):
		"""
		Get orderitem.

		:returns: OrderItem|None
		"""

		return self.get_field('orderitem', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'orderitem' in ret and isinstance(ret['orderitem'], OrderItem):
			ret['orderitem'] = ret['orderitem'].to_dict()

		return ret
