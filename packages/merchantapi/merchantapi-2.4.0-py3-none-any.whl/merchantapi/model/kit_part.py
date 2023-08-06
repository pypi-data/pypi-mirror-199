"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

KitPart data model.
"""

from merchantapi.abstract import Model

class KitPart(Model):
	def __init__(self, data: dict = None):
		"""
		KitPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_part_id(self) -> int:
		"""
		Get part_id.

		:returns: int
		"""

		return self.get_field('part_id', 0)

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def set_part_id(self, part_id: int) -> 'KitPart':
		"""
		Set part_id.

		:param part_id: int
		:returns: KitPart
		"""

		return self.set_field('part_id', part_id)

	def set_quantity(self, quantity: int) -> 'KitPart':
		"""
		Set quantity.

		:param quantity: int
		:returns: KitPart
		"""

		return self.set_field('quantity', quantity)
