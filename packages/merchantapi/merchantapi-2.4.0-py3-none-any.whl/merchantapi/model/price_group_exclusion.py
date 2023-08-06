"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PriceGroupExclusion data model.
"""

from merchantapi.abstract import Model

class PriceGroupExclusion(Model):
	# EXCLUSION_SCOPE constants.
	EXCLUSION_SCOPE_BASKET = 'basket'
	EXCLUSION_SCOPE_GROUP = 'group'
	EXCLUSION_SCOPE_ITEM = 'item'

	def __init__(self, data: dict = None):
		"""
		PriceGroupExclusion Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_scope(self) -> str:
		"""
		Get scope.

		:returns: string
		"""

		return self.get_field('scope')

	def set_id(self, id: int) -> 'PriceGroupExclusion':
		"""
		Set id.

		:param id: int
		:returns: PriceGroupExclusion
		"""

		return self.set_field('id', id)

	def set_scope(self, scope: str) -> 'PriceGroupExclusion':
		"""
		Set scope.

		:param scope: string
		:returns: PriceGroupExclusion
		"""

		return self.set_field('scope', scope)
