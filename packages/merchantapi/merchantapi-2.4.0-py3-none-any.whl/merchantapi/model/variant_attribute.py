"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

VariantAttribute data model.
"""

from merchantapi.abstract import Model

class VariantAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		VariantAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def get_attribute_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_attribute_template_attribute_code(self) -> str:
		"""
		Get attmpat_code.

		:returns: string
		"""

		return self.get_field('attmpat_code')

	def get_option_code(self) -> str:
		"""
		Get option_code.

		:returns: string
		"""

		return self.get_field('option_code')

	def set_attribute_id(self, attribute_id: int) -> 'VariantAttribute':
		"""
		Set attr_id.

		:param attribute_id: int
		:returns: VariantAttribute
		"""

		return self.set_field('attr_id', attribute_id)

	def set_attribute_template_attribute_id(self, attribute_template_attribute_id: int) -> 'VariantAttribute':
		"""
		Set attmpat_id.

		:param attribute_template_attribute_id: int
		:returns: VariantAttribute
		"""

		return self.set_field('attmpat_id', attribute_template_attribute_id)

	def set_option_id(self, option_id: int) -> 'VariantAttribute':
		"""
		Set option_id.

		:param option_id: int
		:returns: VariantAttribute
		"""

		return self.set_field('option_id', option_id)

	def set_attribute_code(self, attribute_code: str) -> 'VariantAttribute':
		"""
		Set attr_code.

		:param attribute_code: string
		:returns: VariantAttribute
		"""

		return self.set_field('attr_code', attribute_code)

	def set_attribute_template_attribute_code(self, attribute_template_attribute_code: str) -> 'VariantAttribute':
		"""
		Set attmpat_code.

		:param attribute_template_attribute_code: string
		:returns: VariantAttribute
		"""

		return self.set_field('attmpat_code', attribute_template_attribute_code)

	def set_option_code(self, option_code: str) -> 'VariantAttribute':
		"""
		Set option_code.

		:param option_code: string
		:returns: VariantAttribute
		"""

		return self.set_field('option_code', option_code)
