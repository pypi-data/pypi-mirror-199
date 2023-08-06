"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CopyPageRule data model.
"""

from merchantapi.abstract import Model

class CopyPageRule(Model):
	# PAGE_RULE_SETTINGS constants.
	PAGE_RULE_SETTINGS_ALL = 'all'
	PAGE_RULE_SETTINGS_NONE = 'none'
	PAGE_RULE_SETTINGS_SPECIFIC = 'specific'

	def __init__(self, data: dict = None):
		"""
		CopyPageRule Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_secure(self) -> bool:
		"""
		Get secure.

		:returns: bool
		"""

		return self.get_field('secure', False)

	def get_title(self) -> bool:
		"""
		Get title.

		:returns: bool
		"""

		return self.get_field('title', False)

	def get_template(self) -> bool:
		"""
		Get template.

		:returns: bool
		"""

		return self.get_field('template', False)

	def get_items(self) -> bool:
		"""
		Get items.

		:returns: bool
		"""

		return self.get_field('items', False)

	def get_settings(self) -> str:
		"""
		Get settings.

		:returns: string
		"""

		return self.get_field('settings')

	def get_javascript_resource_assignments(self) -> bool:
		"""
		Get jsres.

		:returns: bool
		"""

		return self.get_field('jsres', False)

	def get_css_resource_assignments(self) -> bool:
		"""
		Get cssres.

		:returns: bool
		"""

		return self.get_field('cssres', False)

	def get_cache_settings(self) -> bool:
		"""
		Get cacheset.

		:returns: bool
		"""

		return self.get_field('cacheset', False)
