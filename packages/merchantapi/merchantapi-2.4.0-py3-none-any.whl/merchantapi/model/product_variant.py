"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductVariant data model.
"""

from merchantapi.abstract import Model
from .product_variant_part import ProductVariantPart
from .product_variant_dimension import ProductVariantDimension
from .product_variant_attribute import ProductVariantAttribute

class ProductVariant(Model):
	def __init__(self, data: dict = None):
		"""
		ProductVariant Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('parts'):
			value = self.get_field('parts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductVariantPart):
							value[i] = ProductVariantPart(e)
					else:
						raise Exception('Expected list of ProductVariantPart or dict')
			else:
				raise Exception('Expected list of ProductVariantPart or dict')

		if self.has_field('dimensions'):
			value = self.get_field('dimensions')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductVariantDimension):
							value[i] = ProductVariantDimension(e)
					else:
						raise Exception('Expected list of ProductVariantDimension or dict')
			else:
				raise Exception('Expected list of ProductVariantDimension or dict')

		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductVariantAttribute):
							value[i] = ProductVariantAttribute(e)
					else:
						raise Exception('Expected list of ProductVariantAttribute or dict')
			else:
				raise Exception('Expected list of ProductVariantAttribute or dict')

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_variant_id(self) -> int:
		"""
		Get variant_id.

		:returns: int
		"""

		return self.get_field('variant_id', 0)

	def get_parts(self):
		"""
		Get parts.

		:returns: List of ProductVariantPart
		"""

		return self.get_field('parts', [])

	def get_dimensions(self):
		"""
		Get dimensions.

		:returns: List of ProductVariantDimension
		"""

		return self.get_field('dimensions', [])

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductVariantAttribute
		"""

		return self.get_field('attributes', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'parts' in ret and isinstance(ret['parts'], list):
			for i, e in enumerate(ret['parts']):
				if isinstance(e, ProductVariantPart):
					ret['parts'][i] = ret['parts'][i].to_dict()

		if 'dimensions' in ret and isinstance(ret['dimensions'], list):
			for i, e in enumerate(ret['dimensions']):
				if isinstance(e, ProductVariantDimension):
					ret['dimensions'][i] = ret['dimensions'][i].to_dict()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductVariantAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret
