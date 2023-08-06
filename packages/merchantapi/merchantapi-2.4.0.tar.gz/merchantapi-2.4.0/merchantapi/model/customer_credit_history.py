"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomerCreditHistory data model.
"""

from merchantapi.abstract import Model

class CustomerCreditHistory(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerCreditHistory Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_transaction_reference(self) -> str:
		"""
		Get txref.

		:returns: string
		"""

		return self.get_field('txref')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_amount(self) -> float:
		"""
		Get amount.

		:returns: float
		"""

		return self.get_field('amount', 0.00)

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_timestamp_field('dtstamp')

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')
