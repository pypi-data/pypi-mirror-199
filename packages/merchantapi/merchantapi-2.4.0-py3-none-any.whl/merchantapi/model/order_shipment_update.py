"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderShipmentUpdate data model.
"""

from merchantapi.abstract import Model

class OrderShipmentUpdate(Model):
	def __init__(self, data: dict = None):
		"""
		OrderShipmentUpdate Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_shipment_id(self) -> int:
		"""
		Get shpmnt_id.

		:returns: int
		"""

		return self.get_field('shpmnt_id', 0)

	def get_mark_shipped(self) -> bool:
		"""
		Get mark_shipped.

		:returns: bool
		"""

		return self.get_field('mark_shipped', False)

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

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def set_shipment_id(self, shipment_id: int) -> 'OrderShipmentUpdate':
		"""
		Set shpmnt_id.

		:param shipment_id: int
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('shpmnt_id', shipment_id)

	def set_mark_shipped(self, mark_shipped: bool) -> 'OrderShipmentUpdate':
		"""
		Set mark_shipped.

		:param mark_shipped: bool
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('mark_shipped', mark_shipped)

	def set_tracking_number(self, tracking_number: str) -> 'OrderShipmentUpdate':
		"""
		Set tracknum.

		:param tracking_number: string
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('tracknum', tracking_number)

	def set_tracking_type(self, tracking_type: str) -> 'OrderShipmentUpdate':
		"""
		Set tracktype.

		:param tracking_type: string
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('tracktype', tracking_type)

	def set_cost(self, cost: float) -> 'OrderShipmentUpdate':
		"""
		Set cost.

		:param cost: int
		:returns: OrderShipmentUpdate
		"""

		return self.set_field('cost', cost)
