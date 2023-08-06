"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Changeset data model.
"""

from merchantapi.abstract import Model

class Changeset(Model):
	def __init__(self, data: dict = None):
		"""
		Changeset Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_branch_id(self) -> int:
		"""
		Get branch_id.

		:returns: int
		"""

		return self.get_field('branch_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_timestamp_field('dtstamp')

	def get_notes(self) -> str:
		"""
		Get notes.

		:returns: string
		"""

		return self.get_field('notes')

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_tags(self) -> dict:
		"""
		Get tags.

		:returns: dict
		"""

		return self.get_field('tags', {})

	def get_formatted_tags(self) -> str:
		"""
		Get formatted_tags.

		:returns: string
		"""

		return self.get_field('formatted_tags')
