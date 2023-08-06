"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

JavaScriptResourceAttribute data model.
"""

from .resource_attribute import ResourceAttribute

class JavaScriptResourceAttribute(ResourceAttribute):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
