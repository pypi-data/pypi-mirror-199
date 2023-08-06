"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

VariantPart data model.
"""

from merchantapi.abstract import Model

class VariantPart(Model):
	def __init__(self, data: dict = None):
		"""
		VariantPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_part_id(self) -> int:
		"""
		Get part_id.

		:returns: int
		"""

		return self.get_field('part_id', 0)

	def get_part_code(self) -> str:
		"""
		Get part_code.

		:returns: string
		"""

		return self.get_field('part_code')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def set_part_id(self, part_id: int) -> 'VariantPart':
		"""
		Set part_id.

		:param part_id: int
		:returns: VariantPart
		"""

		return self.set_field('part_id', part_id)

	def set_part_code(self, part_code: str) -> 'VariantPart':
		"""
		Set part_code.

		:param part_code: string
		:returns: VariantPart
		"""

		return self.set_field('part_code', part_code)

	def set_quantity(self, quantity: int) -> 'VariantPart':
		"""
		Set quantity.

		:param quantity: int
		:returns: VariantPart
		"""

		return self.set_field('quantity', quantity)
