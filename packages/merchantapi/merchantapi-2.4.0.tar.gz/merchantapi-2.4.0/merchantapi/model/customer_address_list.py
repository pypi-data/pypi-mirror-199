"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomerAddressList data model.
"""

from merchantapi.abstract import Model
from .customer_address import CustomerAddress

class CustomerAddressList(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerAddressList Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('addresses'):
			value = self.get_field('addresses')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, CustomerAddress):
							value[i] = CustomerAddress(e)
					else:
						raise Exception('Expected list of CustomerAddress or dict')
			else:
				raise Exception('Expected list of CustomerAddress or dict')

	def get_ship_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_bill_id(self) -> int:
		"""
		Get bill_id.

		:returns: int
		"""

		return self.get_field('bill_id', 0)

	def get_addresses(self):
		"""
		Get addresses.

		:returns: List of CustomerAddress
		"""

		return self.get_field('addresses', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'addresses' in ret and isinstance(ret['addresses'], list):
			for i, e in enumerate(ret['addresses']):
				if isinstance(e, CustomerAddress):
					ret['addresses'][i] = ret['addresses'][i].to_dict()

		return ret
