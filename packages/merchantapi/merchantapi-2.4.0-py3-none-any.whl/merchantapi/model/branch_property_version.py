"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

BranchPropertyVersion data model.
"""

from .property_version import PropertyVersion

class BranchPropertyVersion(PropertyVersion):
	def __init__(self, data: dict = None):
		"""
		BranchPropertyVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
