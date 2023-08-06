"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderShipmentList_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/ordershipmentlist_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderShipmentListUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OrderShipmentListUpdate Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.shipment_updates = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderShipmentList_Update'

	def get_shipment_updates(self) -> list:
		"""
		Get Shipment_Updates.

		:returns: List of OrderShipmentUpdate
		"""

		return self.shipment_updates

	def set_shipment_updates(self, shipment_updates: list) -> 'OrderShipmentListUpdate':
		"""
		Set Shipment_Updates.

		:param shipment_updates: {OrderShipmentUpdate[]}
		:raises Exception:
		:returns: OrderShipmentListUpdate
		"""

		for e in shipment_updates:
			if not isinstance(e, merchantapi.model.OrderShipmentUpdate):
				raise Exception("")
		self.shipment_updates = shipment_updates
		return self
	
	def add_shipment_update(self, shipment_update) -> 'OrderShipmentListUpdate':
		"""
		Add Shipment_Updates.

		:param shipment_update: OrderShipmentUpdate 
		:raises Exception:
		:returns: {OrderShipmentListUpdate}
		"""

		if isinstance(shipment_update, merchantapi.model.OrderShipmentUpdate):
			self.shipment_updates.append(shipment_update)
		elif isinstance(shipment_update, dict):
			self.shipment_updates.append(merchantapi.model.OrderShipmentUpdate(shipment_update))
		else:
			raise Exception('Expected instance of OrderShipmentUpdate or dict')
		return self

	def add_shipment_updates(self, shipment_updates: list) -> 'OrderShipmentListUpdate':
		"""
		Add many OrderShipmentUpdate.

		:param shipment_updates: List of OrderShipmentUpdate
		:raises Exception:
		:returns: OrderShipmentListUpdate
		"""

		for e in shipment_updates:
			if not isinstance(e, merchantapi.model.OrderShipmentUpdate):
				raise Exception('')
			self.shipment_updates.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderShipmentListUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderShipmentListUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderShipmentListUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if len(self.shipment_updates):
			data['Shipment_Updates'] = []

			for f in self.shipment_updates:
				data['Shipment_Updates'].append(f.to_dict())
		return data
