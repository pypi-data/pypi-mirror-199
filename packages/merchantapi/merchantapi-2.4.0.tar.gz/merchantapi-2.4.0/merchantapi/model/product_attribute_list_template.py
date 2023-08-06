"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductAttributeListTemplate data model.
"""

from merchantapi.abstract import Model

class ProductAttributeListTemplate(Model):
	def __init__(self, data: dict = None):
		"""
		ProductAttributeListTemplate Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_reference_count(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)
