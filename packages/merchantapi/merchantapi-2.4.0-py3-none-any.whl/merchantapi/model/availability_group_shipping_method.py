"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

AvailabilityGroupShippingMethod data model.
"""

from merchantapi.abstract import Model

class AvailabilityGroupShippingMethod(Model):
	def __init__(self, data: dict = None):
		"""
		AvailabilityGroupShippingMethod Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_module_code(self) -> str:
		"""
		Get mod_code.

		:returns: string
		"""

		return self.get_field('mod_code')

	def get_method_code(self) -> str:
		"""
		Get meth_code.

		:returns: string
		"""

		return self.get_field('meth_code')

	def get_method_name(self) -> str:
		"""
		Get method_name.

		:returns: string
		"""

		return self.get_field('method_name')

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)
