"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

DiscountModuleCapabilities data model.
"""

from merchantapi.abstract import Model

class DiscountModuleCapabilities(Model):
	def __init__(self, data: dict = None):
		"""
		DiscountModuleCapabilities Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_preitems(self) -> bool:
		"""
		Get preitems.

		:returns: bool
		"""

		return self.get_field('preitems', False)

	def get_items(self) -> bool:
		"""
		Get items.

		:returns: bool
		"""

		return self.get_field('items', False)

	def get_eligibility(self) -> str:
		"""
		Get eligibility.

		:returns: string
		"""

		return self.get_field('eligibility')

	def get_basket(self) -> bool:
		"""
		Get basket.

		:returns: bool
		"""

		return self.get_field('basket', False)

	def get_shipping(self) -> bool:
		"""
		Get shipping.

		:returns: bool
		"""

		return self.get_field('shipping', False)

	def get_qualifying(self) -> bool:
		"""
		Get qualifying.

		:returns: bool
		"""

		return self.get_field('qualifying', False)
