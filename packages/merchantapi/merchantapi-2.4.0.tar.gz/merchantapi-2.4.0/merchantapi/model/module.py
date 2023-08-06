"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Module data model.
"""

from merchantapi.abstract import Model

class Module(Model):
	def __init__(self, data: dict = None):
		"""
		Module Constructor

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

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_provider(self) -> str:
		"""
		Get provider.

		:returns: string
		"""

		return self.get_field('provider')

	def get_api_version(self) -> str:
		"""
		Get api_ver.

		:returns: string
		"""

		return self.get_field('api_ver')

	def get_version(self) -> str:
		"""
		Get version.

		:returns: string
		"""

		return self.get_field('version')

	def get_module(self) -> str:
		"""
		Get module.

		:returns: string
		"""

		return self.get_field('module')

	def get_reference_count(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)
