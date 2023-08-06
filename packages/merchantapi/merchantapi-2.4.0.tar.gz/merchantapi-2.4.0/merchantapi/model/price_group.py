"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PriceGroup data model.
"""

from merchantapi.abstract import Model
from .module import Module
from .discount_module_capabilities import DiscountModuleCapabilities

class PriceGroup(Model):
	# ELIGIBILITY constants.
	ELIGIBILITY_COUPON = 'C'
	ELIGIBILITY_ALL = 'A'
	ELIGIBILITY_CUSTOMER = 'X'
	ELIGIBILITY_LOGGED_IN = 'L'

	# DISCOUNT_TYPE constants.
	DISCOUNT_TYPE_RETAIL = 'R'
	DISCOUNT_TYPE_COST = 'C'
	DISCOUNT_TYPE_DISCOUNT_RETAIL = 'D'
	DISCOUNT_TYPE_MARKUP_COST = 'M'

	def __init__(self, data: dict = None):
		"""
		PriceGroup Constructor

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

		if self.has_field('capabilities'):
			value = self.get_field('capabilities')
			if isinstance(value, dict):
				if not isinstance(value, DiscountModuleCapabilities):
					self.set_field('capabilities', DiscountModuleCapabilities(value))
			else:
				raise Exception('Expected DiscountModuleCapabilities or a dict')

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

	def get_customer_scope(self) -> str:
		"""
		Get custscope.

		:returns: string
		"""

		return self.get_field('custscope')

	def get_rate(self) -> str:
		"""
		Get rate.

		:returns: string
		"""

		return self.get_field('rate')

	def get_discount(self) -> float:
		"""
		Get discount.

		:returns: float
		"""

		return self.get_field('discount', 0.00)

	def get_markup(self) -> float:
		"""
		Get markup.

		:returns: float
		"""

		return self.get_field('markup', 0.00)

	def get_date_time_start(self) -> int:
		"""
		Get dt_start.

		:returns: int
		"""

		return self.get_timestamp_field('dt_start')

	def get_date_time_end(self) -> int:
		"""
		Get dt_end.

		:returns: int
		"""

		return self.get_timestamp_field('dt_end')

	def get_minimum_subtotal(self) -> float:
		"""
		Get qmn_subtot.

		:returns: float
		"""

		return self.get_field('qmn_subtot', 0.00)

	def get_maximum_subtotal(self) -> float:
		"""
		Get qmx_subtot.

		:returns: float
		"""

		return self.get_field('qmx_subtot', 0.00)

	def get_minimum_quantity(self) -> int:
		"""
		Get qmn_quan.

		:returns: int
		"""

		return self.get_field('qmn_quan', 0)

	def get_maximum_quantity(self) -> int:
		"""
		Get qmx_quan.

		:returns: int
		"""

		return self.get_field('qmx_quan', 0)

	def get_minimum_weight(self) -> float:
		"""
		Get qmn_weight.

		:returns: float
		"""

		return self.get_field('qmn_weight', 0.00)

	def get_maximum_weight(self) -> float:
		"""
		Get qmx_weight.

		:returns: float
		"""

		return self.get_field('qmx_weight', 0.00)

	def get_basket_minimum_subtotal(self) -> float:
		"""
		Get bmn_subtot.

		:returns: float
		"""

		return self.get_field('bmn_subtot', 0.00)

	def get_basket_maximum_subtotal(self) -> float:
		"""
		Get bmx_subtot.

		:returns: float
		"""

		return self.get_field('bmx_subtot', 0.00)

	def get_basket_minimum_quantity(self) -> int:
		"""
		Get bmn_quan.

		:returns: int
		"""

		return self.get_field('bmn_quan', 0)

	def get_basket_maximum_quantity(self) -> int:
		"""
		Get bmx_quan.

		:returns: int
		"""

		return self.get_field('bmx_quan', 0)

	def get_basket_minimum_weight(self) -> float:
		"""
		Get bmn_weight.

		:returns: float
		"""

		return self.get_field('bmn_weight', 0.00)

	def get_basket_maximum_weight(self) -> float:
		"""
		Get bmx_weight.

		:returns: float
		"""

		return self.get_field('bmx_weight', 0.00)

	def get_priority(self) -> int:
		"""
		Get priority.

		:returns: int
		"""

		return self.get_field('priority', 0)

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def get_capabilities(self):
		"""
		Get capabilities.

		:returns: DiscountModuleCapabilities|None
		"""

		return self.get_field('capabilities', None)

	def get_exclusion(self) -> bool:
		"""
		Get exclusion.

		:returns: bool
		"""

		return self.get_field('exclusion', False)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_display(self) -> bool:
		"""
		Get display.

		:returns: bool
		"""

		return self.get_field('display', False)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		if 'capabilities' in ret and isinstance(ret['capabilities'], DiscountModuleCapabilities):
			ret['capabilities'] = ret['capabilities'].to_dict()

		return ret
