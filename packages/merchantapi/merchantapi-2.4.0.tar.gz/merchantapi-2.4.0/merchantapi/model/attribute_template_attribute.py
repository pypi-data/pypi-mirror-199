"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

AttributeTemplateAttribute data model.
"""

from merchantapi.abstract import Model
from .attribute_template_option import AttributeTemplateOption

class AttributeTemplateAttribute(Model):
	# TEMPLATE_ATTRIBUTE_TYPE constants.
	TEMPLATE_ATTRIBUTE_TYPE_CHECKBOX = 'checkbox'
	TEMPLATE_ATTRIBUTE_TYPE_RADIO = 'radio'
	TEMPLATE_ATTRIBUTE_TYPE_TEXT = 'text'
	TEMPLATE_ATTRIBUTE_TYPE_SELECT = 'select'
	TEMPLATE_ATTRIBUTE_TYPE_MEMO = 'memo'
	TEMPLATE_ATTRIBUTE_TYPE_TEMPLATE = 'template'
	TEMPLATE_ATTRIBUTE_TYPE_SWATCH_SELECT = 'swatch-select'

	def __init__(self, data: dict = None):
		"""
		AttributeTemplateAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, AttributeTemplateOption):
							value[i] = AttributeTemplateOption(e)
					else:
						raise Exception('Expected list of AttributeTemplateOption or dict')
			else:
				raise Exception('Expected list of AttributeTemplateOption or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_default_id(self) -> int:
		"""
		Get default_id.

		:returns: int
		"""

		return self.get_field('default_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

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

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_required(self) -> bool:
		"""
		Get required.

		:returns: bool
		"""

		return self.get_field('required', False)

	def get_inventory(self) -> bool:
		"""
		Get inventory.

		:returns: bool
		"""

		return self.get_field('inventory', False)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_options(self):
		"""
		Get options.

		:returns: List of AttributeTemplateOption
		"""

		return self.get_field('options', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, AttributeTemplateOption):
					ret['options'][i] = ret['options'][i].to_dict()

		return ret
