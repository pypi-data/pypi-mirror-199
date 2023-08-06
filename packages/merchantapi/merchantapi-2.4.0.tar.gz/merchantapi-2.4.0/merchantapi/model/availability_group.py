"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

AvailabilityGroup data model.
"""

from merchantapi.abstract import Model

class AvailabilityGroup(Model):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroup Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)
