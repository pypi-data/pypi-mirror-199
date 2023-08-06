"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderPaymentAuthorize data model.
"""

from merchantapi.abstract import Model

class OrderPaymentAuthorize(Model):
	def __init__(self, data: dict = None):
		"""
		OrderPaymentAuthorize Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_valid(self) -> bool:
		"""
		Get valid.

		:returns: bool
		"""

		return self.get_field('valid', False)

	def get_total_authorized(self) -> float:
		"""
		Get total_auth.

		:returns: float
		"""

		return self.get_field('total_auth', 0.00)

	def get_formatted_total_authorized(self) -> str:
		"""
		Get formatted_total_auth.

		:returns: string
		"""

		return self.get_field('formatted_total_auth')

	def get_total_captured(self) -> float:
		"""
		Get total_capt.

		:returns: float
		"""

		return self.get_field('total_capt', 0.00)

	def get_formatted_total_captured(self) -> str:
		"""
		Get formatted_total_capt.

		:returns: string
		"""

		return self.get_field('formatted_total_capt')

	def get_total_refunded(self) -> float:
		"""
		Get total_rfnd.

		:returns: float
		"""

		return self.get_field('total_rfnd', 0.00)

	def get_formatted_total_refunded(self) -> str:
		"""
		Get formatted_total_rfnd.

		:returns: string
		"""

		return self.get_field('formatted_total_rfnd')

	def get_net_captured(self) -> float:
		"""
		Get net_capt.

		:returns: float
		"""

		return self.get_field('net_capt', 0.00)

	def get_formatted_net_captured(self) -> str:
		"""
		Get formatted_net_capt.

		:returns: string
		"""

		return self.get_field('formatted_net_capt')
