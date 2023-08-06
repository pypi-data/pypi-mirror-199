"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderItemDiscount data model.
"""

from merchantapi.abstract import Model

class OrderItemDiscount(Model):
	def __init__(self, data: dict = None):
		"""
		OrderItemDiscount Constructor

		:param data: dict
		"""

		super().__init__(data)

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

	def get_price_group_id(self) -> int:
		"""
		Get pgrp_id.

		:returns: int
		"""

		return self.get_field('pgrp_id', 0)

	def get_display(self) -> bool:
		"""
		Get display.

		:returns: bool
		"""

		return self.get_field('display', False)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_discount(self) -> float:
		"""
		Get discount.

		:returns: float
		"""

		return self.get_field('discount', 0.00)
