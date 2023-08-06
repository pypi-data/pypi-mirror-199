"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Page data model.
"""

from merchantapi.abstract import Model
from .version_settings import VersionSettings
from .uri import Uri
from .custom_field_values import CustomFieldValues

class Page(Model):
	# PAGE_CACHE_TYPE constants.
	PAGE_CACHE_TYPE_NEVER = 'never'
	PAGE_CACHE_TYPE_PROVISIONAL = 'provisional'
	PAGE_CACHE_TYPE_ANONEMPTY = 'anonempty'
	PAGE_CACHE_TYPE_ALLEMPTY = 'allempty'
	PAGE_CACHE_TYPE_ALWAYS = 'always'

	def __init__(self, data: dict = None):
		"""
		Page Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, VersionSettings):
				self.set_field('settings', VersionSettings(value))

		if self.has_field('uris'):
			value = self.get_field('uris')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Uri):
							value[i] = Uri(e)
					else:
						raise Exception('Expected list of Uri or dict')
			else:
				raise Exception('Expected list of Uri or dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_secure(self) -> bool:
		"""
		Get secure.

		:returns: bool
		"""

		return self.get_field('secure', False)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_title(self) -> str:
		"""
		Get title.

		:returns: string
		"""

		return self.get_field('title')

	def get_ui_id(self) -> int:
		"""
		Get ui_id.

		:returns: int
		"""

		return self.get_field('ui_id', 0)

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_admin(self) -> bool:
		"""
		Get admin.

		:returns: bool
		"""

		return self.get_field('admin', False)

	def get_layout(self) -> bool:
		"""
		Get layout.

		:returns: bool
		"""

		return self.get_field('layout', False)

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

	def get_cache(self) -> str:
		"""
		Get cache.

		:returns: string
		"""

		return self.get_field('cache')

	def get_url(self) -> str:
		"""
		Get url.

		:returns: string
		"""

		return self.get_field('url')

	def get_uris(self):
		"""
		Get uris.

		:returns: List of Uri
		"""

		return self.get_field('uris', [])

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], VersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		if 'uris' in ret and isinstance(ret['uris'], list):
			for i, e in enumerate(ret['uris']):
				if isinstance(e, Uri):
					ret['uris'][i] = ret['uris'][i].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		return ret
