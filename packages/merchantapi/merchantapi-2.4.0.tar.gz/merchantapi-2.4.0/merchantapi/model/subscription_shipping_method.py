"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

SubscriptionShippingMethod data model.
"""

from merchantapi.abstract import Model
from .module import Module

class SubscriptionShippingMethod(Model):
	def __init__(self, data: dict = None):
		"""
		SubscriptionShippingMethod Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('module'):
			value = self.get_field('module')
			if isinstance(value, dict):
				if not isinstance(value, Module):
					self.set_field('module', Module(value))
			else:
				raise Exception('Expected Module or a dict')

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def get_method_code(self) -> str:
		"""
		Get method_code.

		:returns: string
		"""

		return self.get_field('method_code')

	def get_method_name(self) -> str:
		"""
		Get method_name.

		:returns: string
		"""

		return self.get_field('method_name')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		return ret
