"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductSubscriptionSettings data model.
"""

from merchantapi.abstract import Model

class ProductSubscriptionSettings(Model):
	def __init__(self, data: dict = None):
		"""
		ProductSubscriptionSettings Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_enabled(self) -> bool:
		"""
		Get enabled.

		:returns: bool
		"""

		return self.get_field('enabled', False)

	def get_mandatory(self) -> bool:
		"""
		Get mandatory.

		:returns: bool
		"""

		return self.get_field('mandatory', False)

	def get_can_cancel(self) -> bool:
		"""
		Get can_cancel.

		:returns: bool
		"""

		return self.get_field('can_cancel', False)

	def get_cancel_minimum_required_orders(self) -> int:
		"""
		Get cncl_min.

		:returns: int
		"""

		return self.get_field('cncl_min', 0)

	def get_can_change_quantities(self) -> bool:
		"""
		Get can_qty.

		:returns: bool
		"""

		return self.get_field('can_qty', False)

	def get_quantities_minimum_required_orders(self) -> int:
		"""
		Get qty_min.

		:returns: int
		"""

		return self.get_field('qty_min', 0)

	def get_can_change_term(self) -> bool:
		"""
		Get can_term.

		:returns: bool
		"""

		return self.get_field('can_term', False)

	def get_term_minimum_required_orders(self) -> int:
		"""
		Get term_min.

		:returns: int
		"""

		return self.get_field('term_min', 0)

	def get_can_change_next_delivery_date(self) -> bool:
		"""
		Get can_date.

		:returns: bool
		"""

		return self.get_field('can_date', False)

	def get_next_delivery_date_minimum_required_orders(self) -> int:
		"""
		Get date_min.

		:returns: int
		"""

		return self.get_field('date_min', 0)
