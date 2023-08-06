"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ChangesetJavaScriptResourceVersion data model.
"""

from .javascript_resource_version import JavaScriptResourceVersion

class ChangesetJavaScriptResourceVersion(JavaScriptResourceVersion):
	def __init__(self, data: dict = None):
		"""
		ChangesetJavaScriptResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
