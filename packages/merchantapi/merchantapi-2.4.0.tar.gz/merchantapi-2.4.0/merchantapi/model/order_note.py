"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderNote data model.
"""

from .note import Note

class OrderNote(Note):
	def __init__(self, data: dict = None):
		"""
		OrderNote Constructor

		:param data: dict
		"""

		super().__init__(data)
