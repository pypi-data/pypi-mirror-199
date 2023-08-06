"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductAndSubscriptionTerm data model.
"""

from .product import Product

class ProductAndSubscriptionTerm(Product):
	def __init__(self, data: dict = None):
		"""
		ProductAndSubscriptionTerm Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_term_id(self) -> int:
		"""
		Get term_id.

		:returns: int
		"""

		return self.get_field('term_id', 0)

	def get_term_frequency(self) -> str:
		"""
		Get term_frequency.

		:returns: string
		"""

		return self.get_field('term_frequency')

	def get_term_term(self) -> int:
		"""
		Get term_term.

		:returns: int
		"""

		return self.get_field('term_term', 0)

	def get_term_description(self) -> str:
		"""
		Get term_descrip.

		:returns: string
		"""

		return self.get_field('term_descrip')

	def get_term_n(self) -> int:
		"""
		Get term_n.

		:returns: int
		"""

		return self.get_field('term_n', 0)

	def get_term_fixed_day_of_week(self) -> int:
		"""
		Get term_fixed_dow.

		:returns: int
		"""

		return self.get_field('term_fixed_dow', 0)

	def get_term_fixed_day_of_month(self) -> int:
		"""
		Get term_fixed_dom.

		:returns: int
		"""

		return self.get_field('term_fixed_dom', 0)

	def get_term_subscription_count(self) -> int:
		"""
		Get term_sub_count.

		:returns: int
		"""

		return self.get_field('term_sub_count', 0)
