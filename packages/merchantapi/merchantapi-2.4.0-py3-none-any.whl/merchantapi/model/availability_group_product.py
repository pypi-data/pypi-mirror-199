"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

AvailabilityGroupProduct data model.
"""

from .product import Product

class AvailabilityGroupProduct(Product):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)
