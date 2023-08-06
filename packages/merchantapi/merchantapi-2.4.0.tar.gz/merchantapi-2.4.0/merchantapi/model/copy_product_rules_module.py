"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CopyProductRulesModule data model.
"""

from merchantapi.abstract import Model
from .module import Module

class CopyProductRulesModule(Model):
	def __init__(self, data: dict = None):
		"""
		CopyProductRulesModule Constructor

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

	def get_rules_id(self) -> int:
		"""
		Get rules_id.

		:returns: int
		"""

		return self.get_field('rules_id', 0)

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		return ret
