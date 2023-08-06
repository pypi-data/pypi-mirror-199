"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

TemplateChange data model.
"""

from merchantapi.abstract import Model
from .version_settings import VersionSettings

class TemplateChange(Model):
	def __init__(self, data: dict = None):
		"""
		TemplateChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Settings'):
			value = self.get_field('Settings')
			if not isinstance(value, VersionSettings):
				self.set_field('Settings', VersionSettings(value))

	def get_template_id(self) -> int:
		"""
		Get Template_ID.

		:returns: int
		"""

		return self.get_field('Template_ID', 0)

	def get_template_filename(self) -> str:
		"""
		Get Template_Filename.

		:returns: string
		"""

		return self.get_field('Template_Filename')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_settings(self):
		"""
		Get Settings.

		:returns: VersionSettings|None
		"""

		return self.get_field('Settings', None)

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_template_id(self, template_id: int) -> 'TemplateChange':
		"""
		Set Template_ID.

		:param template_id: int
		:returns: TemplateChange
		"""

		return self.set_field('Template_ID', template_id)

	def set_template_filename(self, template_filename: str) -> 'TemplateChange':
		"""
		Set Template_Filename.

		:param template_filename: string
		:returns: TemplateChange
		"""

		return self.set_field('Template_Filename', template_filename)

	def set_source(self, source: str) -> 'TemplateChange':
		"""
		Set Source.

		:param source: string
		:returns: TemplateChange
		"""

		return self.set_field('Source', source)

	def set_settings(self, settings) -> 'TemplateChange':
		"""
		Set Settings.

		:param settings: VersionSettings|dict
		:returns: TemplateChange
		:raises Exception:
		"""

		if settings is None or isinstance(settings, VersionSettings):
			return self.set_field('Settings', settings)
		return self.set_field('Settings', VersionSettings(settings))

	def set_notes(self, notes: str) -> 'TemplateChange':
		"""
		Set Notes.

		:param notes: string
		:returns: TemplateChange
		"""

		return self.set_field('Notes', notes)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Settings' in ret and isinstance(ret['Settings'], VersionSettings):
			ret['Settings'] = ret['Settings'].to_dict()

		return ret
