"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

BranchJavaScriptResourceVersion data model.
"""

from .javascript_resource_version import JavaScriptResourceVersion

class BranchJavaScriptResourceVersion(JavaScriptResourceVersion):
	def __init__(self, data: dict = None):
		"""
		BranchJavaScriptResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
