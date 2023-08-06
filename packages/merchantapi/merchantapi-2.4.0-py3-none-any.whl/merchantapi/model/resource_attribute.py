"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ResourceAttribute data model.
"""

from merchantapi.abstract import Model

class ResourceAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		ResourceAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_value(self) -> str:
		"""
		Get value.

		:returns: string
		"""

		return self.get_field('value')

	def set_name(self, name: str) -> 'ResourceAttribute':
		"""
		Set name.

		:param name: string
		:returns: ResourceAttribute
		"""

		return self.set_field('name', name)

	def set_value(self, value: str) -> 'ResourceAttribute':
		"""
		Set value.

		:param value: string
		:returns: ResourceAttribute
		"""

		return self.set_field('value', value)
