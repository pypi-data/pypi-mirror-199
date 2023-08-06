"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderProduct data model.
"""

from merchantapi.abstract import Model
from .order_product_attribute import OrderProductAttribute

class OrderProduct(Model):
	def __init__(self, data: dict = None):
		"""
		OrderProduct Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderProductAttribute):
							value[i] = OrderProductAttribute(e)
					else:
						raise Exception('Expected list of OrderProductAttribute or dict')
			else:
				raise Exception('Expected list of OrderProductAttribute or dict')

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_tracking_number(self) -> str:
		"""
		Get tracknum.

		:returns: string
		"""

		return self.get_field('tracknum')

	def get_tracking_type(self) -> str:
		"""
		Get tracktype.

		:returns: string
		"""

		return self.get_field('tracktype')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of OrderProductAttribute
		"""

		return self.get_field('attributes', [])

	def set_status(self, status: int) -> 'OrderProduct':
		"""
		Set status.

		:param status: int
		:returns: OrderProduct
		"""

		return self.set_field('status', status)

	def set_code(self, code: str) -> 'OrderProduct':
		"""
		Set code.

		:param code: string
		:returns: OrderProduct
		"""

		return self.set_field('code', code)

	def set_sku(self, sku: str) -> 'OrderProduct':
		"""
		Set sku.

		:param sku: string
		:returns: OrderProduct
		"""

		return self.set_field('sku', sku)

	def set_tracking_number(self, tracking_number: str) -> 'OrderProduct':
		"""
		Set tracknum.

		:param tracking_number: string
		:returns: OrderProduct
		"""

		return self.set_field('tracknum', tracking_number)

	def set_tracking_type(self, tracking_type: str) -> 'OrderProduct':
		"""
		Set tracktype.

		:param tracking_type: string
		:returns: OrderProduct
		"""

		return self.set_field('tracktype', tracking_type)

	def set_quantity(self, quantity: int) -> 'OrderProduct':
		"""
		Set quantity.

		:param quantity: int
		:returns: OrderProduct
		"""

		return self.set_field('quantity', quantity)

	def set_attributes(self, attributes: list) -> 'OrderProduct':
		"""
		Set attributes.

		:param attributes: List of OrderProductAttribute 
		:raises Exception:
		:returns: OrderProduct
		"""

		for i, e in enumerate(attributes, 0):
			if isinstance(e, OrderProductAttribute):
				continue
			elif isinstance(e, dict):
				attributes[i] = OrderProductAttribute(e)
			else:
				raise Exception('Expected instance of OrderProductAttribute or dict')
		return self.set_field('attributes', attributes)
	
	def add_attribute(self, attribute: 'OrderProductAttribute') -> 'OrderProduct':
		"""
		Add a OrderProductAttribute.
		
		:param attribute: OrderProductAttribute
		:returns: OrderProduct
		"""

		if 'attributes' not in self:
			self['attributes'] = []
		self['attributes'].append(attribute)
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, OrderProductAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		return ret
