"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CSSResourceChange data model.
"""

from merchantapi.abstract import Model
from .css_resource_version_attribute import CSSResourceVersionAttribute

class CSSResourceChange(Model):
	def __init__(self, data: dict = None):
		"""
		CSSResourceChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Attributes'):
			value = self.get_field('Attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CSSResourceVersionAttribute):
							value[i] = CSSResourceVersionAttribute(e)
					else:
						raise Exception('Expected list of CSSResourceVersionAttribute or dict')
			else:
				raise Exception('Expected list of CSSResourceVersionAttribute or dict')

	def get_css_resource_id(self) -> int:
		"""
		Get CSSResource_ID.

		:returns: int
		"""

		return self.get_field('CSSResource_ID', 0)

	def get_css_resource_code(self) -> str:
		"""
		Get CSSResource_Code.

		:returns: string
		"""

		return self.get_field('CSSResource_Code')

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

		:returns: List of CSSResourceVersionAttribute
		"""

		return self.get_field('Attributes', [])

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_css_resource_id(self, css_resource_id: int) -> 'CSSResourceChange':
		"""
		Set CSSResource_ID.

		:param css_resource_id: int
		:returns: CSSResourceChange
		"""

		return self.set_field('CSSResource_ID', css_resource_id)

	def set_css_resource_code(self, css_resource_code: str) -> 'CSSResourceChange':
		"""
		Set CSSResource_Code.

		:param css_resource_code: string
		:returns: CSSResourceChange
		"""

		return self.set_field('CSSResource_Code', css_resource_code)

	def set_type(self, type: str) -> 'CSSResourceChange':
		"""
		Set Type.

		:param type: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Type', type)

	def set_is_global(self, is_global: bool) -> 'CSSResourceChange':
		"""
		Set Global.

		:param is_global: bool
		:returns: CSSResourceChange
		"""

		return self.set_field('Global', is_global)

	def set_active(self, active: bool) -> 'CSSResourceChange':
		"""
		Set Active.

		:param active: bool
		:returns: CSSResourceChange
		"""

		return self.set_field('Active', active)

	def set_file_path(self, file_path: str) -> 'CSSResourceChange':
		"""
		Set File_Path.

		:param file_path: string
		:returns: CSSResourceChange
		"""

		return self.set_field('File_Path', file_path)

	def set_branchless_file_path(self, branchless_file_path: str) -> 'CSSResourceChange':
		"""
		Set Branchless_File_Path.

		:param branchless_file_path: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Branchless_File_Path', branchless_file_path)

	def set_source(self, source: str) -> 'CSSResourceChange':
		"""
		Set Source.

		:param source: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Source', source)

	def set_linked_pages(self, linked_pages) -> 'CSSResourceChange':
		"""
		Set LinkedPages.

		:param linked_pages: list
		:returns: CSSResourceChange
		"""

		return self.set_field('LinkedPages', linked_pages)

	def set_linked_resources(self, linked_resources) -> 'CSSResourceChange':
		"""
		Set LinkedResources.

		:param linked_resources: list
		:returns: CSSResourceChange
		"""

		return self.set_field('LinkedResources', linked_resources)

	def set_attributes(self, attributes: list) -> 'CSSResourceChange':
		"""
		Set Attributes.

		:param attributes: List of CSSResourceVersionAttribute 
		:raises Exception:
		:returns: CSSResourceChange
		"""

		for i, e in enumerate(attributes, 0):
			if isinstance(e, CSSResourceVersionAttribute):
				continue
			elif isinstance(e, dict):
				attributes[i] = CSSResourceVersionAttribute(e)
			else:
				raise Exception('Expected instance of CSSResourceVersionAttribute or dict')
		return self.set_field('Attributes', attributes)

	def set_notes(self, notes: str) -> 'CSSResourceChange':
		"""
		Set Notes.

		:param notes: string
		:returns: CSSResourceChange
		"""

		return self.set_field('Notes', notes)
	
	def add_attribute(self, attribute: 'CSSResourceVersionAttribute') -> 'CSSResourceChange':
		"""
		Add a CSSResourceVersionAttribute.
		
		:param attribute: CSSResourceVersionAttribute
		:returns: CSSResourceChange
		"""

		if 'Attributes' not in self:
			self['Attributes'] = []
		self['Attributes'].append(attribute)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Attributes' in ret and isinstance(ret['Attributes'], list):
			for i, e in enumerate(ret['Attributes']):
				if isinstance(e, CSSResourceVersionAttribute):
					ret['Attributes'][i] = ret['Attributes'][i].to_dict()

		return ret
