"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

JavaScriptResource data model.
"""

from merchantapi.abstract import Model
from .javascript_resource_attribute import JavaScriptResourceAttribute

class JavaScriptResource(Model):
	# RESOURCE_TYPE constants.
	RESOURCE_TYPE_COMBINED = 'C'
	RESOURCE_TYPE_INLINE = 'I'
	RESOURCE_TYPE_EXTERNAL = 'E'
	RESOURCE_TYPE_LOCAL = 'L'

	def __init__(self, data: dict = None):
		"""
		JavaScriptResource Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResourceAttribute):
							value[i] = JavaScriptResourceAttribute(e)
					else:
						raise Exception('Expected list of JavaScriptResourceAttribute or dict')
			else:
				raise Exception('Expected list of JavaScriptResourceAttribute or dict')

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

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of JavaScriptResourceAttribute
		"""

		return self.get_field('attributes', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, JavaScriptResourceAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret
