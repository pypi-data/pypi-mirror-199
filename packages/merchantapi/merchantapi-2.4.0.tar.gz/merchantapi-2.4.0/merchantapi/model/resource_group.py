"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ResourceGroup data model.
"""

from merchantapi.abstract import Model
from .css_resource import CSSResource
from .javascript_resource import JavaScriptResource

class ResourceGroup(Model):
	def __init__(self, data: dict = None):
		"""
		ResourceGroup Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('linkedcssresources'):
			value = self.get_field('linkedcssresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResource):
							value[i] = CSSResource(e)
					else:
						raise Exception('Expected list of CSSResource or dict')
			else:
				raise Exception('Expected list of CSSResource or dict')

		if self.has_field('linkedjavascriptresources'):
			value = self.get_field('linkedjavascriptresources')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResource):
							value[i] = JavaScriptResource(e)
					else:
						raise Exception('Expected list of JavaScriptResource or dict')
			else:
				raise Exception('Expected list of JavaScriptResource or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_linked_css_resources(self):
		"""
		Get linkedcssresources.

		:returns: List of CSSResource
		"""

		return self.get_field('linkedcssresources', [])

	def get_linked_javascript_resources(self):
		"""
		Get linkedjavascriptresources.

		:returns: List of JavaScriptResource
		"""

		return self.get_field('linkedjavascriptresources', [])

	def get_linked_java_script_resources(self):
		# Alias of get_linked_javascript_resources
		return self.get_linked_javascript_resources()

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'linkedcssresources' in ret and isinstance(ret['linkedcssresources'], list):
			for i, e in enumerate(ret['linkedcssresources']):
				if isinstance(e, CSSResource):
					ret['linkedcssresources'][i] = ret['linkedcssresources'][i].to_dict()

		if 'linkedjavascriptresources' in ret and isinstance(ret['linkedjavascriptresources'], list):
			for i, e in enumerate(ret['linkedjavascriptresources']):
				if isinstance(e, JavaScriptResource):
					ret['linkedjavascriptresources'][i] = ret['linkedjavascriptresources'][i].to_dict()

		return ret
