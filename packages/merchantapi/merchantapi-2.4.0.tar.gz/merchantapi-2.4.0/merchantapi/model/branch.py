"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Branch data model.
"""

from merchantapi.abstract import Model

class Branch(Model):
	def __init__(self, data: dict = None):
		"""
		Branch Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_immutable(self) -> bool:
		"""
		Get immutable.

		:returns: bool
		"""

		return self.get_field('immutable', False)

	def get_branch_key(self) -> str:
		"""
		Get branchkey.

		:returns: string
		"""

		return self.get_field('branchkey')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_color(self) -> str:
		"""
		Get color.

		:returns: string
		"""

		return self.get_field('color')

	def get_framework(self) -> str:
		"""
		Get framework.

		:returns: string
		"""

		return self.get_field('framework')

	def get_is_primary(self) -> bool:
		"""
		Get is_primary.

		:returns: bool
		"""

		return self.get_field('is_primary', False)

	def get_is_working(self) -> bool:
		"""
		Get is_working.

		:returns: bool
		"""

		return self.get_field('is_working', False)

	def get_preview_url(self) -> str:
		"""
		Get preview_url.

		:returns: string
		"""

		return self.get_field('preview_url')
