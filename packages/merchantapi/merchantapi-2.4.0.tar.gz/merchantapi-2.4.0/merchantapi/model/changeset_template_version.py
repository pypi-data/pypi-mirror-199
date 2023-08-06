"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ChangesetTemplateVersion data model.
"""

from merchantapi.abstract import Model
from .version_settings import VersionSettings

class ChangesetTemplateVersion(Model):
	def __init__(self, data: dict = None):
		"""
		ChangesetTemplateVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, VersionSettings):
				self.set_field('settings', VersionSettings(value))

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_parent_id(self) -> int:
		"""
		Get parent_id.

		:returns: int
		"""

		return self.get_field('parent_id', 0)

	def get_item_id(self) -> int:
		"""
		Get item_id.

		:returns: int
		"""

		return self.get_field('item_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

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

	def get_property_id(self) -> int:
		"""
		Get prop_id.

		:returns: int
		"""

		return self.get_field('prop_id', 0)

	def get_sync(self) -> bool:
		"""
		Get sync.

		:returns: bool
		"""

		return self.get_field('sync', False)

	def get_filename(self) -> str:
		"""
		Get filename.

		:returns: string
		"""

		return self.get_field('filename')

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

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_settings(self):
		"""
		Get settings.

		:returns: VersionSettings|None
		"""

		return self.get_field('settings', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], VersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		return ret
