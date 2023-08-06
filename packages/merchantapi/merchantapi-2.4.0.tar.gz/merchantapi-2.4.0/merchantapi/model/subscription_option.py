"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

SubscriptionOption data model.
"""

from merchantapi.abstract import Model

class SubscriptionOption(Model):
	def __init__(self, data: dict = None):
		"""
		SubscriptionOption Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_subscription_id(self) -> int:
		"""
		Get subscrp_id.

		:returns: int
		"""

		return self.get_field('subscrp_id', 0)

	def get_template_code(self) -> str:
		"""
		Get templ_code.

		:returns: string
		"""

		return self.get_field('templ_code')

	def get_attribute_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')
