"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductInventoryAdjustment data model.
"""

from merchantapi.abstract import Model

class ProductInventoryAdjustment(Model):
	def __init__(self, data: dict = None):
		"""
		ProductInventoryAdjustment Constructor

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

	def get_product_sku(self) -> str:
		"""
		Get product_sku.

		:returns: string
		"""

		return self.get_field('product_sku')

	def get_adjustment(self) -> float:
		"""
		Get adjustment.

		:returns: float
		"""

		return self.get_field('adjustment', 0.00)

	def set_product_id(self, product_id: int) -> 'ProductInventoryAdjustment':
		"""
		Set product_id.

		:param product_id: int
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('product_id', product_id)

	def set_product_code(self, product_code: str) -> 'ProductInventoryAdjustment':
		"""
		Set product_code.

		:param product_code: string
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('product_code', product_code)

	def set_product_sku(self, product_sku: str) -> 'ProductInventoryAdjustment':
		"""
		Set product_sku.

		:param product_sku: string
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('product_sku', product_sku)

	def set_adjustment(self, adjustment: float) -> 'ProductInventoryAdjustment':
		"""
		Set adjustment.

		:param adjustment: int
		:returns: ProductInventoryAdjustment
		"""

		return self.set_field('adjustment', adjustment)
