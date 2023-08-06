"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ReceivedReturn data model.
"""

from merchantapi.abstract import Model

class ReceivedReturn(Model):
	def __init__(self, data: dict = None):
		"""
		ReceivedReturn Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_return_id(self) -> int:
		"""
		Get return_id.

		:returns: int
		"""

		return self.get_field('return_id', 0)

	def get_adjust_inventory(self) -> int:
		"""
		Get adjust_inventory.

		:returns: int
		"""

		return self.get_field('adjust_inventory', 0)

	def set_return_id(self, return_id: int) -> 'ReceivedReturn':
		"""
		Set return_id.

		:param return_id: int
		:returns: ReceivedReturn
		"""

		return self.set_field('return_id', return_id)

	def set_adjust_inventory(self, adjust_inventory: int) -> 'ReceivedReturn':
		"""
		Set adjust_inventory.

		:param adjust_inventory: int
		:returns: ReceivedReturn
		"""

		return self.set_field('adjust_inventory', adjust_inventory)
