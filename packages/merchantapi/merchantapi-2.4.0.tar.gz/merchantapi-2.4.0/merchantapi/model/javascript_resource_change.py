"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

JavaScriptResourceChange data model.
"""

from merchantapi.abstract import Model
from .javascript_resource_version_attribute import JavaScriptResourceVersionAttribute

class JavaScriptResourceChange(Model):
	def __init__(self, data: dict = None):
		"""
		JavaScriptResourceChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Attributes'):
			value = self.get_field('Attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, JavaScriptResourceVersionAttribute):
							value[i] = JavaScriptResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of JavaScriptResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of JavaScriptResourceVersionAttribute or dict')

	def get_javascript_resource_id(self) -> int:
		"""
		Get JavaScriptResource_ID.

		:returns: int
		"""

		return self.get_field('JavaScriptResource_ID', 0)

	def get_javascript_resource_code(self) -> str:
		"""
		Get JavaScriptResource_Code.

		:returns: string
		"""

		return self.get_field('JavaScriptResource_Code')

	def get_type(self) -> str:
		"""
		Get Type.

		:returns: string
		"""

		return self.get_field('Type')

	def get_is_global(self) -> bool:
		"""
		Get Global.

		:returns: bool
		"""

		return self.get_field('Global', False)

	def get_active(self) -> bool:
		"""
		Get Active.

		:returns: bool
		"""

		return self.get_field('Active', False)

	def get_file_path(self) -> str:
		"""
		Get File_Path.

		:returns: string
		"""

		return self.get_field('File_Path')

	def get_branchless_file_path(self) -> str:
		"""
		Get Branchless_File_Path.

		:returns: string
		"""

		return self.get_field('Branchless_File_Path')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_linked_pages(self) -> dict:
		"""
		Get LinkedPages.

		:returns: dict
		"""

		return self.get_field('LinkedPages', {})

	def get_linked_resources(self) -> dict:
		"""
		Get LinkedResources.

		:returns: dict
		"""

		return self.get_field('LinkedResources', {})

	def get_attributes(self):
		"""
		Get Attributes.

		:returns: List of JavaScriptResourceVersionAttribute
		"""

		return self.get_field('Attributes', [])

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_javascript_resource_id(self, javascript_resource_id: int) -> 'JavaScriptResourceChange':
		"""
		Set JavaScriptResource_ID.

		:param javascript_resource_id: int
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('JavaScriptResource_ID', javascript_resource_id)

	def set_javascript_resource_code(self, javascript_resource_code: str) -> 'JavaScriptResourceChange':
		"""
		Set JavaScriptResource_Code.

		:param javascript_resource_code: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('JavaScriptResource_Code', javascript_resource_code)

	def set_type(self, type: str) -> 'JavaScriptResourceChange':
		"""
		Set Type.

		:param type: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Type', type)

	def set_is_global(self, is_global: bool) -> 'JavaScriptResourceChange':
		"""
		Set Global.

		:param is_global: bool
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Global', is_global)

	def set_active(self, active: bool) -> 'JavaScriptResourceChange':
		"""
		Set Active.

		:param active: bool
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Active', active)

	def set_file_path(self, file_path: str) -> 'JavaScriptResourceChange':
		"""
		Set File_Path.

		:param file_path: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('File_Path', file_path)

	def set_branchless_file_path(self, branchless_file_path: str) -> 'JavaScriptResourceChange':
		"""
		Set Branchless_File_Path.

		:param branchless_file_path: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Branchless_File_Path', branchless_file_path)

	def set_source(self, source: str) -> 'JavaScriptResourceChange':
		"""
		Set Source.

		:param source: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Source', source)

	def set_linked_pages(self, linked_pages) -> 'JavaScriptResourceChange':
		"""
		Set LinkedPages.

		:param linked_pages: list
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('LinkedPages', linked_pages)

	def set_linked_resources(self, linked_resources) -> 'JavaScriptResourceChange':
		"""
		Set LinkedResources.

		:param linked_resources: list
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('LinkedResources', linked_resources)

	def set_attributes(self, attributes: list) -> 'JavaScriptResourceChange':
		"""
		Set Attributes.

		:param attributes: List of JavaScriptResourceVersionAttribute 
		:raises Exception:
		:returns: JavaScriptResourceChange
		"""

		for i, e in enumerate(attributes, 0):
			if isinstance(e, JavaScriptResourceVersionAttribute):
				continue
			elif isinstance(e, dict):
				attributes[i] = JavaScriptResourceVersionAttribute(e)
			else:
				raise Exception('Expected instance of JavaScriptResourceVersionAttribute or dict')
		return self.set_field('Attributes', attributes)

	def set_notes(self, notes: str) -> 'JavaScriptResourceChange':
		"""
		Set Notes.

		:param notes: string
		:returns: JavaScriptResourceChange
		"""

		return self.set_field('Notes', notes)
	
	def add_attribute(self, attribute: 'JavaScriptResourceVersionAttribute') -> 'JavaScriptResourceChange':
		"""
		Add a JavaScriptResourceVersionAttribute.
		
		:param attribute: JavaScriptResourceVersionAttribute
		:returns: JavaScriptResourceChange
		"""

		if 'Attributes' not in self:
			self['Attributes'] = []
		self['Attributes'].append(attribute)
		return self

	def get_java_script_resource_id(self) -> int:
		# Alias of get_javascript_resource_id
		return self.get_javascript_resource_id()

	def get_java_script_resource_code(self) -> str:
		# Alias of get_javascript_resource_code
		return self.get_javascript_resource_code()

	def set_java_script_resource_id(self, java_script_resource_id: int) -> 'JavaScriptResourceChange':
		# Alias of set_javascript_resource_id
		return self.set_javascript_resource_id(java_script_resource_id)

	def set_java_script_resource_code(self, java_script_resource_code: str) -> 'JavaScriptResourceChange':
		# Alias of set_javascript_resource_code
		return self.set_javascript_resource_code(java_script_resource_code)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Attributes' in ret and isinstance(ret['Attributes'], list):
			for i, e in enumerate(ret['Attributes']):
				if isinstance(e, JavaScriptResourceVersionAttribute):
					ret['Attributes'][i] = ret['Attributes'][i].to_dict()

		return ret
