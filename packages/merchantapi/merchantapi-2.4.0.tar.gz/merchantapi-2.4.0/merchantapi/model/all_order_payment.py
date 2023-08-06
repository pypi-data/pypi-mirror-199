"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

AllOrderPayment data model.
"""

from .order import Order
from .order_payment import OrderPayment

class AllOrderPayment(Order):
	def __init__(self, data: dict = None):
		"""
		AllOrderPayment Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('orderpayment'):
			value = self.get_field('orderpayment')
			if isinstance(value, dict):
				if not isinstance(value, OrderPayment):
					self.set_field('orderpayment', OrderPayment(value))
			else:
				raise Exception('Expected OrderPayment or a dict')

	def get_order_payment(self):
		"""
		Get orderpayment.

		:returns: OrderPayment|None
		"""

		return self.get_field('orderpayment', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'orderpayment' in ret and isinstance(ret['orderpayment'], OrderPayment):
			ret['orderpayment'] = ret['orderpayment'].to_dict()

		return ret
