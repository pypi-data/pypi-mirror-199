"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderPayment data model.
"""

from merchantapi.abstract import Model

class OrderPayment(Model):
	# ORDER_PAYMENT_TYPE constants.
	ORDER_PAYMENT_TYPE_DECLINED = 0
	ORDER_PAYMENT_TYPE_LEGACY_AUTH = 1
	ORDER_PAYMENT_TYPE_LEGACY_CAPTURE = 2
	ORDER_PAYMENT_TYPE_AUTH = 3
	ORDER_PAYMENT_TYPE_CAPTURE = 4
	ORDER_PAYMENT_TYPE_AUTH_CAPTURE = 5
	ORDER_PAYMENT_TYPE_REFUND = 6
	ORDER_PAYMENT_TYPE_VOID = 7

	def __init__(self, data: dict = None):
		"""
		OrderPayment Constructor

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

		return self.get_timestamp_field('dtstamp')

	def get_expires(self) -> int:
		"""
		Get expires.

		:returns: int
		"""

		return self.get_timestamp_field('expires')

	def get_payment_id(self) -> int:
		"""
		Get pay_id.

		:returns: int
		"""

		return self.get_field('pay_id', 0)

	def get_payment_sec_id(self) -> int:
		"""
		Get pay_secid.

		:returns: int
		"""

		return self.get_field('pay_secid', 0)

	def get_decrypt_status(self) -> str:
		"""
		Get decrypt_status.

		:returns: string
		"""

		return self.get_field('decrypt_status')

	def get_decrypt_error(self) -> str:
		"""
		Get decrypt_error.

		:returns: string
		"""

		return self.get_field('decrypt_error')

	def get_description(self) -> str:
		"""
		Get description.

		:returns: string
		"""

		return self.get_field('description')

	def get_payment_data(self) -> dict:
		"""
		Get data.

		:returns: dict
		"""

		return self.get_field('data', {})

	def get_ip(self) -> str:
		"""
		Get ip.

		:returns: string
		"""

		return self.get_field('ip')
