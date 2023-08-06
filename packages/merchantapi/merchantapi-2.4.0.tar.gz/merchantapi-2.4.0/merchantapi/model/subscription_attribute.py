"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

SubscriptionAttribute data model.
"""

from merchantapi.abstract import Model

class SubscriptionAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		SubscriptionAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_template_code(self) -> str:
		"""
		Get template_code.

		:returns: string
		"""

		return self.get_field('template_code')

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')

	def set_code(self, code: str) -> 'SubscriptionAttribute':
		"""
		Set code.

		:param code: string
		:returns: SubscriptionAttribute
		"""

		return self.set_field('code', code)

	def set_template_code(self, template_code: str) -> 'SubscriptionAttribute':
		"""
		Set template_code.

		:param template_code: string
		:returns: SubscriptionAttribute
		"""

		return self.set_field('template_code', template_code)

	def set_value(self, value: str) -> 'SubscriptionAttribute':
		"""
		Set value.

		:param value: string
		:returns: SubscriptionAttribute
		"""

		return self.set_field('value', value)
