"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProvisionMessage data model.
"""

from merchantapi.abstract import Model

class ProvisionMessage(Model):
	def __init__(self, data: dict = None):
		"""
		ProvisionMessage Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_date_time_stamp(self) -> str:
		"""
		Get dtstamp.

		:returns: string
		"""

		return self.get_field('dtstamp')

	def get_line_number(self) -> int:
		"""
		Get lineno.

		:returns: int
		"""

		return self.get_field('lineno', 0)

	def get_tag(self) -> str:
		"""
		Get tag.

		:returns: string
		"""

		return self.get_field('tag')

	def get_message(self) -> str:
		"""
		Get message.

		:returns: string
		"""

		return self.get_field('message')
