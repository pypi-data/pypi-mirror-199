"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductShippingRules data model.
"""

from merchantapi.abstract import Model
from .product_shipping_method import ProductShippingMethod

class ProductShippingRules(Model):
	def __init__(self, data: dict = None):
		"""
		ProductShippingRules Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('methods'):
			value = self.get_field('methods')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductShippingMethod):
							value[i] = ProductShippingMethod(e)
					else:
						raise Exception('Expected list of ProductShippingMethod or dict')
			else:
				raise Exception('Expected list of ProductShippingMethod or dict')

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_own_package(self) -> bool:
		"""
		Get ownpackage.

		:returns: bool
		"""

		return self.get_field('ownpackage', False)

	def get_width(self) -> float:
		"""
		Get width.

		:returns: float
		"""

		return self.get_field('width', 0.00)

	def get_length(self) -> float:
		"""
		Get length.

		:returns: float
		"""

		return self.get_field('length', 0.00)

	def get_height(self) -> float:
		"""
		Get height.

		:returns: float
		"""

		return self.get_field('height', 0.00)

	def get_limit_methods(self) -> bool:
		"""
		Get limitmeths.

		:returns: bool
		"""

		return self.get_field('limitmeths', False)

	def get_methods(self):
		"""
		Get methods.

		:returns: List of ProductShippingMethod
		"""

		return self.get_field('methods', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'methods' in ret and isinstance(ret['methods'], list):
			for i, e in enumerate(ret['methods']):
				if isinstance(e, ProductShippingMethod):
					ret['methods'][i] = ret['methods'][i].to_dict()

		return ret
