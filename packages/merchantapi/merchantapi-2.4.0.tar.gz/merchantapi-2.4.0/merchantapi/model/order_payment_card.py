"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderPaymentCard data model.
"""

from .customer_payment_card import CustomerPaymentCard

class OrderPaymentCard(CustomerPaymentCard):
	def __init__(self, data: dict = None):
		"""
		OrderPaymentCard Constructor

		:param data: dict
		"""

		super().__init__(data)
