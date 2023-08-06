"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

BusinessAccount data model.
"""

from merchantapi.abstract import Model

class BusinessAccount(Model):
	def __init__(self, data: dict = None):
		"""
		BusinessAccount Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_title(self) -> str:
		"""
		Get title.

		:returns: string
		"""

		return self.get_field('title')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)

	def get_order_count(self) -> int:
		"""
		Get order_cnt.

		:returns: int
		"""

		return self.get_field('order_cnt', 0)

	def get_order_average(self) -> float:
		"""
		Get order_avg.

		:returns: float
		"""

		return self.get_field('order_avg', 0.00)

	def get_formatted_order_average(self) -> str:
		"""
		Get formatted_order_avg.

		:returns: string
		"""

		return self.get_field('formatted_order_avg')

	def get_order_total(self) -> float:
		"""
		Get order_tot.

		:returns: float
		"""

		return self.get_field('order_tot', 0.00)

	def get_formatted_order_total(self) -> str:
		"""
		Get formatted_order_tot.

		:returns: string
		"""

		return self.get_field('formatted_order_tot')

	def get_note_count(self) -> int:
		"""
		Get note_count.

		:returns: int
		"""

		return self.get_field('note_count', 0)
