"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

SplitOrderItem data model.
"""

from merchantapi.abstract import Model
from .order_item import OrderItem

class SplitOrderItem(Model):
	def __init__(self, data: dict = None):
		"""
		SplitOrderItem Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('original_orderitem'):
			value = self.get_field('original_orderitem')
			if isinstance(value, dict):
				if not isinstance(value, OrderItem):
					self.set_field('original_orderitem', OrderItem(value))
			else:
				raise Exception('Expected OrderItem or a dict')

		if self.has_field('split_orderitem'):
			value = self.get_field('split_orderitem')
			if isinstance(value, dict):
				if not isinstance(value, OrderItem):
					self.set_field('split_orderitem', OrderItem(value))
			else:
				raise Exception('Expected OrderItem or a dict')

	def get_original_order_item(self):
		"""
		Get original_orderitem.

		:returns: OrderItem|None
		"""

		return self.get_field('original_orderitem', None)

	def get_split_order_item(self):
		"""
		Get split_orderitem.

		:returns: OrderItem|None
		"""

		return self.get_field('split_orderitem', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'original_orderitem' in ret and isinstance(ret['original_orderitem'], OrderItem):
			ret['original_orderitem'] = ret['original_orderitem'].to_dict()

		if 'split_orderitem' in ret and isinstance(ret['split_orderitem'], OrderItem):
			ret['split_orderitem'] = ret['split_orderitem'].to_dict()

		return ret
