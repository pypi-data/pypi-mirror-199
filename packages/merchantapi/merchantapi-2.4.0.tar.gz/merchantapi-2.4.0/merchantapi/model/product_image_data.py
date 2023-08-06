"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductImageData data model.
"""

from merchantapi.abstract import Model

class ProductImageData(Model):
	def __init__(self, data: dict = None):
		"""
		ProductImageData Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_image_id(self) -> int:
		"""
		Get image_id.

		:returns: int
		"""

		return self.get_field('image_id', 0)

	def get_type_id(self) -> int:
		"""
		Get type_id.

		:returns: int
		"""

		return self.get_field('type_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type_description(self) -> str:
		"""
		Get type_desc.

		:returns: string
		"""

		return self.get_field('type_desc')

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_width(self) -> int:
		"""
		Get width.

		:returns: int
		"""

		return self.get_field('width', 0)

	def get_height(self) -> int:
		"""
		Get height.

		:returns: int
		"""

		return self.get_field('height', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)
