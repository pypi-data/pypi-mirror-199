"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderCustomField data model.
"""

from merchantapi.abstract import Model
from .module import Module

class OrderCustomField(Model):
	def __init__(self, data: dict = None):
		"""
		OrderCustomField Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('module'):
			value = self.get_field('module')
			if isinstance(value, dict):
				if not isinstance(value, Module):
					self.set_field('module', Module(value))
			else:
				raise Exception('Expected Module or a dict')

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

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_searchable(self) -> bool:
		"""
		Get searchable.

		:returns: bool
		"""

		return self.get_field('searchable', False)

	def get_sortable(self) -> bool:
		"""
		Get sortable.

		:returns: bool
		"""

		return self.get_field('sortable', False)

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def get_choices(self) -> dict:
		"""
		Get choices.

		:returns: dict
		"""

		return self.get_field('choices', {})

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		return ret
