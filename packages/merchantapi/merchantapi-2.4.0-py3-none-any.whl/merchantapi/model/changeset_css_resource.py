"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ChangesetCSSResource data model.
"""

from .css_resource import CSSResource

class ChangesetCSSResource(CSSResource):
	def __init__(self, data: dict = None):
		"""
		ChangesetCSSResource Constructor

		:param data: dict
		"""

		super().__init__(data)
