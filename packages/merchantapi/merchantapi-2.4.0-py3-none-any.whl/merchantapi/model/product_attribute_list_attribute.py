"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductAttributeListAttribute data model.
"""

from merchantapi.abstract import Model
from .product_option import ProductOption
from .product_attribute_list_template import ProductAttributeListTemplate

class ProductAttributeListAttribute(Model):
	def __init__(self, data: dict = None):
		"""
		ProductAttributeListAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductAttributeListAttribute):
							value[i] = ProductAttributeListAttribute(e)
					else:
						raise Exception('Expected list of ProductAttributeListAttribute or dict')
			else:
				raise Exception('Expected list of ProductAttributeListAttribute or dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductOption):
							value[i] = ProductOption(e)
					else:
						raise Exception('Expected list of ProductOption or dict')
			else:
				raise Exception('Expected list of ProductOption or dict')

		if self.has_field('template'):
			value = self.get_field('template')
			if isinstance(value, dict):
				if not isinstance(value, ProductAttributeListTemplate):
					self.set_field('template', ProductAttributeListTemplate(value))
			else:
				raise Exception('Expected ProductAttributeListTemplate or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

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

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

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

	def get_template_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductAttributeListAttribute
		"""

		return self.get_field('attributes', [])

	def get_options(self):
		"""
		Get options.

		:returns: List of ProductOption
		"""

		return self.get_field('options', [])

	def get_has_variant_parts(self) -> bool:
		"""
		Get has_variant_parts.

		:returns: bool
		"""

		return self.get_field('has_variant_parts', False)

	def get_template(self):
		"""
		Get template.

		:returns: ProductAttributeListTemplate|None
		"""

		return self.get_field('template', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductAttributeListAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, ProductOption):
					ret['options'][i] = ret['options'][i].to_dict()

		if 'template' in ret and isinstance(ret['template'], ProductAttributeListTemplate):
			ret['template'] = ret['template'].to_dict()

		return ret
