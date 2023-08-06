"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderProductAttribute data model.
"""

from merchantapi.abstract import Model

class OrderProductAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		OrderProductAttribute Constructor

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

	def set_code(self, code: str) -> 'OrderProductAttribute':
		"""
		Set code.

		:param code: string
		:returns: OrderProductAttribute
		"""

		return self.set_field('code', code)

	def set_template_code(self, template_code: str) -> 'OrderProductAttribute':
		"""
		Set template_code.

		:param template_code: string
		:returns: OrderProductAttribute
		"""

		return self.set_field('template_code', template_code)

	def set_value(self, value: str) -> 'OrderProductAttribute':
		"""
		Set value.

		:param value: string
		:returns: OrderProductAttribute
		"""

		return self.set_field('value', value)
