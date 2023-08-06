"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductInventorySettings data model.
"""

from merchantapi.abstract import Model

class ProductInventorySettings(Model):
	def __init__(self, data: dict = None):
		"""
		ProductInventorySettings Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_in_stock_message_short(self) -> str:
		"""
		Get in_short.

		:returns: string
		"""

		return self.get_field('in_short')

	def get_in_stock_message_long(self) -> str:
		"""
		Get in_long.

		:returns: string
		"""

		return self.get_field('in_long')

	def get_track_low_stock_level(self) -> str:
		"""
		Get low_track.

		:returns: string
		"""

		return self.get_field('low_track')

	def get_low_stock_level(self) -> int:
		"""
		Get low_level.

		:returns: int
		"""

		return self.get_field('low_level', 0)

	def get_low_stock_level_default(self) -> bool:
		"""
		Get low_lvl_d.

		:returns: bool
		"""

		return self.get_field('low_lvl_d', False)

	def get_low_stock_message_short(self) -> str:
		"""
		Get low_short.

		:returns: string
		"""

		return self.get_field('low_short')

	def get_low_stock_message_long(self) -> str:
		"""
		Get low_long.

		:returns: string
		"""

		return self.get_field('low_long')

	def get_track_out_of_stock_level(self) -> str:
		"""
		Get out_track.

		:returns: string
		"""

		return self.get_field('out_track')

	def get_hide_out_of_stock(self) -> str:
		"""
		Get out_hide.

		:returns: string
		"""

		return self.get_field('out_hide')

	def get_out_of_stock_level(self) -> int:
		"""
		Get out_level.

		:returns: int
		"""

		return self.get_field('out_level', 0)

	def get_out_of_stock_level_default(self) -> bool:
		"""
		Get out_lvl_d.

		:returns: bool
		"""

		return self.get_field('out_lvl_d', False)

	def get_out_of_stock_message_short(self) -> str:
		"""
		Get out_short.

		:returns: string
		"""

		return self.get_field('out_short')

	def get_out_of_stock_message_long(self) -> str:
		"""
		Get out_long.

		:returns: string
		"""

		return self.get_field('out_long')

	def get_limited_stock_message(self) -> str:
		"""
		Get ltd_long.

		:returns: string
		"""

		return self.get_field('ltd_long')
