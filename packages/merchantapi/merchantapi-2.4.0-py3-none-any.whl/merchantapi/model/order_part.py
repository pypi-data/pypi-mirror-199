"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderPart data model.
"""

from merchantapi.abstract import Model

class OrderPart(Model):
	def __init__(self, data: dict = None):
		"""
		OrderPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_total_quantity(self) -> int:
		"""
		Get total_quantity.

		:returns: int
		"""

		return self.get_field('total_quantity', 0)

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)
