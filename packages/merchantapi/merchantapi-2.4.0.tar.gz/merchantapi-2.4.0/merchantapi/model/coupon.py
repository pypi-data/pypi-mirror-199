"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Coupon data model.
"""

from merchantapi.abstract import Model

class Coupon(Model):
	# CUSTOMER_SCOPE constants.
	CUSTOMER_SCOPE_ALL_SHOPPERS = 'A'
	CUSTOMER_SCOPE_SPECIFIC_CUSTOMERS = 'X'
	CUSTOMER_SCOPE_ALL_LOGGED_IN = 'L'

	def __init__(self, data: dict = None):
		"""
		Coupon Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_customer_scope(self) -> str:
		"""
		Get custscope.

		:returns: string
		"""

		return self.get_field('custscope')

	def get_date_time_start(self) -> int:
		"""
		Get dt_start.

		:returns: int
		"""

		return self.get_timestamp_field('dt_start')

	def get_date_time_end(self) -> int:
		"""
		Get dt_end.

		:returns: int
		"""

		return self.get_timestamp_field('dt_end')

	def get_max_use(self) -> int:
		"""
		Get max_use.

		:returns: int
		"""

		return self.get_field('max_use', 0)

	def get_max_per(self) -> int:
		"""
		Get max_per.

		:returns: int
		"""

		return self.get_field('max_per', 0)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_use_count(self) -> int:
		"""
		Get use_count.

		:returns: int
		"""

		return self.get_field('use_count', 0)
