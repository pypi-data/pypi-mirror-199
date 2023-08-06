"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderTotal data model.
"""

from merchantapi.abstract import Model

class OrderTotal(Model):
	def __init__(self, data: dict = None):
		"""
		OrderTotal Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_formatted_total(self) -> str:
		"""
		Get formatted_total.

		:returns: string
		"""

		return self.get_field('formatted_total')
