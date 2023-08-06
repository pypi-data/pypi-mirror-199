"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CSSResourceVersion data model.
"""

from merchantapi.abstract import Model
from .css_resource_version_attribute import CSSResourceVersionAttribute
from .page import Page
from .css_resource import CSSResource

class CSSResourceVersion(Model):
	def __init__(self, data: dict = None):
		"""
		CSSResourceVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResourceVersionAttribute):
							value[i] = CSSResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of CSSResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of CSSResourceVersionAttribute or dict')

		if self.has_field('linkedpages'):
			value = self.get_field('linkedpages')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Page):
							value[i] = Page(e)
					else:
						raise Exception('Expected list of Page or dict')
			else:
				raise Exception('Expected list of Page or dict')

		if self.has_field('linkedresources'):
			value = self.get_field('linkedresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResource):
							value[i] = CSSResource(e)
					else:
						raise Exception('Expected list of CSSResource or dict')
			else:
				raise Exception('Expected list of CSSResource or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_resource_id(self) -> int:
		"""
		Get res_id.

		:returns: int
		"""

		return self.get_field('res_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_is_global(self) -> bool:
		"""
		Get is_global.

		:returns: bool
		"""

		return self.get_field('is_global', False)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_file(self) -> str:
		"""
		Get file.

		:returns: string
		"""

		return self.get_field('file')

	def get_branchless_file(self) -> str:
		"""
		Get branchless_file.

		:returns: string
		"""

		return self.get_field('branchless_file')

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

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

	def get_source_user_id(self) -> int:
		"""
		Get source_user_id.

		:returns: int
		"""

		return self.get_field('source_user_id', 0)

	def get_source_user_name(self) -> str:
		"""
		Get source_user_name.

		:returns: string
		"""

		return self.get_field('source_user_name')

	def get_source_user_icon(self) -> str:
		"""
		Get source_user_icon.

		:returns: string
		"""

		return self.get_field('source_user_icon')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of CSSResourceVersionAttribute
		"""

		return self.get_field('attributes', [])

	def get_linked_pages(self):
		"""
		Get linkedpages.

		:returns: List of Page
		"""

		return self.get_field('linkedpages', [])

	def get_linked_resources(self):
		"""
		Get linkedresources.

		:returns: List of CSSResource
		"""

		return self.get_field('linkedresources', [])

	def get_source_notes(self) -> str:
		"""
		Get source_notes.

		:returns: string
		"""

		return self.get_field('source_notes')

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, CSSResourceVersionAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'linkedpages' in ret and isinstance(ret['linkedpages'], list):
			for i, e in enumerate(ret['linkedpages']):
				if isinstance(e, Page):
					ret['linkedpages'][i] = ret['linkedpages'][i].to_dict()

		if 'linkedresources' in ret and isinstance(ret['linkedresources'], list):
			for i, e in enumerate(ret['linkedresources']):
				if isinstance(e, CSSResource):
					ret['linkedresources'][i] = ret['linkedresources'][i].to_dict()

		return ret
