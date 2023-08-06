"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

AllOrderPaymentData data model.
"""

from merchantapi.abstract import Model

class AllOrderPaymentData(Model):
	def __init__(self, data: dict = None):
		"""
		AllOrderPaymentData Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_type(self) -> int:
		"""
		Get type.

		:returns: int
		"""

		return self.get_field('type', 0)

	def get_reference_number(self) -> str:
		"""
		Get refnum.

		:returns: string
		"""

		return self.get_field('refnum')

	def get_amount(self) -> float:
		"""
		Get amount.

		:returns: float
		"""

		return self.get_field('amount', 0.00)

	def get_formatted_amount(self) -> str:
		"""
		Get formatted_amount.

		:returns: string
		"""

		return self.get_field('formatted_amount')

	def get_available(self) -> float:
		"""
		Get available.

		:returns: float
		"""

		return self.get_field('available', 0.00)

	def get_formatted_available(self) -> str:
		"""
		Get formatted_available.

		:returns: string
		"""

		return self.get_field('formatted_available')

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_field('dtstamp', 0)

	def get_ip(self) -> str:
		"""
		Get ip.

		:returns: string
		"""

		return self.get_field('ip')
