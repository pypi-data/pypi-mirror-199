"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderReturn data model.
"""

from merchantapi.abstract import Model

class OrderReturn(Model):
	# ORDER_RETURN_STATUS constants.
	ORDER_RETURN_STATUS_ISSUED = 500
	ORDER_RETURN_STATUS_RECEIVED = 600

	def __init__(self, data: dict = None):
		"""
		OrderReturn Constructor

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

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_date_time_issued(self) -> int:
		"""
		Get dt_issued.

		:returns: int
		"""

		return self.get_timestamp_field('dt_issued')

	def get_date_time_received(self) -> int:
		"""
		Get dt_recvd.

		:returns: int
		"""

		return self.get_timestamp_field('dt_recvd')
