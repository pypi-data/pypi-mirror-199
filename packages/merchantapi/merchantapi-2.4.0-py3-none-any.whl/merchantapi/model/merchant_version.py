"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

MerchantVersion data model.
"""

from merchantapi.abstract import Model

class MerchantVersion(Model):
	def __init__(self, data: dict = None):
		"""
		MerchantVersion Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_version(self) -> str:
		"""
		Get version.

		:returns: string
		"""

		return self.get_field('version')

	def get_major(self) -> int:
		"""
		Get major.

		:returns: int
		"""

		return self.get_field('major', 0)

	def get_minor(self) -> int:
		"""
		Get minor.

		:returns: int
		"""

		return self.get_field('minor', 0)

	def get_bugfix(self) -> int:
		"""
		Get bugfix.

		:returns: int
		"""

		return self.get_field('bugfix', 0)
