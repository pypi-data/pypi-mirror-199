"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

JavaScriptResourceVersionAttribute data model.
"""

from .resource_attribute import ResourceAttribute

class JavaScriptResourceVersionAttribute(ResourceAttribute):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceVersionAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
