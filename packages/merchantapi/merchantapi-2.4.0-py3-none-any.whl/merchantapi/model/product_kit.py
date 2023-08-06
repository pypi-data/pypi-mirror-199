"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductKit data model.
"""

from merchantapi.abstract import Model
from .product_kit_part import ProductKitPart

class ProductKit(Model):
	def __init__(self, data: dict = None):
		"""
		ProductKit Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('parts'):
			value = self.get_field('parts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductKitPart):
							value[i] = ProductKitPart(e)
					else:
						raise Exception('Expected list of ProductKitPart or dict')
			else:
				raise Exception('Expected list of ProductKitPart or dict')

	def get_attribute_id(self) -> int:
		"""
		Get attr_id.

		:returns: int
		"""

		return self.get_field('attr_id', 0)

	def get_attribute_type(self) -> str:
		"""
		Get attr_type.

		:returns: string
		"""

		return self.get_field('attr_type')

	def get_attribute_code(self) -> str:
		"""
		Get attr_code.

		:returns: string
		"""

		return self.get_field('attr_code')

	def get_attribute_prompt(self) -> str:
		"""
		Get attr_prompt.

		:returns: string
		"""

		return self.get_field('attr_prompt')

	def get_attribute_template_attribute_id(self) -> int:
		"""
		Get attmpat_id.

		:returns: int
		"""

		return self.get_field('attmpat_id', 0)

	def get_option_id(self) -> int:
		"""
		Get option_id.

		:returns: int
		"""

		return self.get_field('option_id', 0)

	def get_option_code(self) -> str:
		"""
		Get option_code.

		:returns: string
		"""

		return self.get_field('option_code')

	def get_option_prompt(self) -> str:
		"""
		Get option_prompt.

		:returns: string
		"""

		return self.get_field('option_prompt')

	def get_option_display_order(self) -> int:
		"""
		Get option_disp_order.

		:returns: int
		"""

		return self.get_field('option_disp_order', 0)

	def get_parts(self):
		"""
		Get parts.

		:returns: List of ProductKitPart
		"""

		return self.get_field('parts', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'parts' in ret and isinstance(ret['parts'], list):
			for i, e in enumerate(ret['parts']):
				if isinstance(e, ProductKitPart):
					ret['parts'][i] = ret['parts'][i].to_dict()

		return ret
