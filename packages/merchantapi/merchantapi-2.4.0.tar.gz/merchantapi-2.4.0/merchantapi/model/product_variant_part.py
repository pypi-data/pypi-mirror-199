"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductVariantPart data model.
"""

from merchantapi.abstract import Model

class ProductVariantPart(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariantPart Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_product_code(self) -> str:
		"""
		Get product_code.

		:returns: string
		"""

		return self.get_field('product_code')

	def get_product_name(self) -> str:
		"""
		Get product_name.

		:returns: string
		"""

		return self.get_field('product_name')

	def get_product_sku(self) -> str:
		"""
		Get product_sku.

		:returns: string
		"""

		return self.get_field('product_sku')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_offset(self) -> int:
		"""
		Get offset.

		:returns: int
		"""

		return self.get_field('offset', 0)
