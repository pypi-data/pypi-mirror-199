"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomFieldValues data model.
"""

from merchantapi.abstract import Model

class CustomFieldValues(Model):
	def __init__(self, data: dict = None):
		"""
		CustomFieldValues Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_value(self, code: str, module : str = 'customfields'):
		"""
		Get a value for a module by its code.

		:param code: str
		:param module: str
		:returns: mixed
		"""

		return self[module][code] if self.has_value(code, module) else None

	def has_value(self, code: str, module: str = 'customfields'):
		"""
		Check if a value for code and module exists.

		:param code: {string}
		:param module: {string}
		:returns: bool
		"""

		if self.has_field(module):
			return code in self.get_field(module)

	def has_module(self, module: str):
		"""
		Check if a specific module is defined.

		:param module: str
		:returns: boolean
		"""

		return self.has_field(module)

	def get_module(self, module: str):
		"""
		Get a specific modules custom field values.

		:param module: str
		:returns: dict
		"""

		return self.get_field(module, {})

	def add_value(self, field: str, value, module: str = 'customfields') -> 'CustomFieldValues':
		"""
		Add a custom field value.

		:param field: str
		:param value: mixed
		:param module: std
		:returns: CustomFieldValues
		"""

		if not self.has_module(module):
			self.set_field(module, {})
		self[module][field] = value
		return self
