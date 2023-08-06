"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductSubscriptionTermDate data model.
"""

from merchantapi.abstract import Model

class ProductSubscriptionTermDate(Model):
	def __init__(self, data: dict = None):
		"""
		ProductSubscriptionTermDate Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_subscription_term_id(self) -> int:
		"""
		Get subterm_id.

		:returns: int
		"""

		return self.get_field('subterm_id', 0)

	def get_term_day_of_month(self) -> int:
		"""
		Get term_dom.

		:returns: int
		"""

		return self.get_field('term_dom', 0)

	def get_term_month(self) -> int:
		"""
		Get term_mon.

		:returns: int
		"""

		return self.get_field('term_mon', 0)
