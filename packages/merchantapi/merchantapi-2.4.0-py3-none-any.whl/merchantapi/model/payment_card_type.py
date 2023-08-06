"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PaymentCardType data model.
"""

from merchantapi.abstract import Model

class PaymentCardType(Model):
	def __init__(self, data: dict = None):
		"""
		PaymentCardType Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_prefixes(self) -> str:
		"""
		Get prefixes.

		:returns: string
		"""

		return self.get_field('prefixes')

	def get_lengths(self) -> str:
		"""
		Get lengths.

		:returns: string
		"""

		return self.get_field('lengths')

	def get_cvv(self) -> bool:
		"""
		Get cvv.

		:returns: bool
		"""

		return self.get_field('cvv', False)
