"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderItemOption data model.
"""

from merchantapi.abstract import Model
from .order_item_option_discount import OrderItemOptionDiscount

class OrderItemOption(Model):
	def __init__(self, data: dict = None):
		"""
		OrderItemOption Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('discounts'):
			value = self.get_field('discounts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItemOptionDiscount):
							value[i] = OrderItemOptionDiscount(e)
					else:
						raise Exception('Expected list of OrderItemOptionDiscount or dict')
			else:
				raise Exception('Expected list of OrderItemOptionDiscount or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

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

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def get_option_code(self) -> str:
		"""
		Get opt_code.

		:returns: string
		"""

		return self.get_field('opt_code')

	def get_attribute_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

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

	def get_option_data(self) -> str:
		"""
		Get data.

		:returns: string
		"""

		return self.get_field('data')

	def get_option_data_long(self) -> str:
		"""
		Get data_long.

		:returns: string
		"""

		return self.get_field('data_long')

	def get_attribute_prompt(self) -> str:
		"""
		Get attr_prompt.

		:returns: string
		"""

		return self.get_field('attr_prompt')

	def get_option_prompt(self) -> str:
		"""
		Get opt_prompt.

		:returns: string
		"""

		return self.get_field('opt_prompt')

	def get_discounts(self):
		"""
		Get discounts.

		:returns: List of OrderItemOptionDiscount
		"""

		return self.get_field('discounts', [])

	def set_attribute_code(self, attribute_code: str) -> 'OrderItemOption':
		"""
		Set attr_code.

		:param attribute_code: string
		:returns: OrderItemOption
		"""

		return self.set_field('attr_code', attribute_code)

	def set_attribute_id(self, attribute_id: int) -> 'OrderItemOption':
		"""
		Set attr_id.

		:param attribute_id: int
		:returns: OrderItemOption
		"""

		return self.set_field('attr_id', attribute_id)

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'OrderItemOption':
		"""
		Set attmpat_id.

		:param attribute_template_attribute_id: int
		:returns: OrderItemOption
		"""

		return self.set_field('attmpat_id', attribute_template_attribute_id)

	def set_value(self, value: str) -> 'OrderItemOption':
		"""
		Set value.

		:param value: string
		:returns: OrderItemOption
		"""

		return self.set_field('value', value)

	def set_weight(self, weight: float) -> 'OrderItemOption':
		"""
		Set weight.

		:param weight: int
		:returns: OrderItemOption
		"""

		return self.set_field('weight', weight)

	def set_retail(self, retail: float) -> 'OrderItemOption':
		"""
		Set retail.

		:param retail: int
		:returns: OrderItemOption
		"""

		return self.set_field('retail', retail)

	def set_base_price(self, base_price: float) -> 'OrderItemOption':
		"""
		Set base_price.

		:param base_price: int
		:returns: OrderItemOption
		"""

		return self.set_field('base_price', base_price)

	def set_price(self, price: float) -> 'OrderItemOption':
		"""
		Set price.

		:param price: int
		:returns: OrderItemOption
		"""

		return self.set_field('price', price)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = {}

		if self.has_field('attr_code'):
			ret['attr_code'] = self.get_field('attr_code')

		if self.has_field('attr_id'):
			ret['attr_id'] = self.get_field('attr_id')

		if self.has_field('attmpat_id'):
			ret['attmpat_id'] = self.get_field('attmpat_id')

		if self.has_field('value'):
			ret['opt_code_or_data'] = self.get_field('value')

		if self.has_field('price'):
			ret['price'] = self.get_field('price')

		if self.has_field('weight'):
			ret['weight'] = self.get_field('weight')

		return ret
