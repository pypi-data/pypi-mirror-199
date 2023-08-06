"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductList_Adjust_Inventory. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productlist_adjust_inventory
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductListAdjustInventory(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProductListAdjustInventory Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.inventory_adjustments = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductList_Adjust_Inventory'

	def get_inventory_adjustments(self) -> list:
		"""
		Get Inventory_Adjustments.

		:returns: List of ProductInventoryAdjustment
		"""

		return self.inventory_adjustments

	def set_inventory_adjustments(self, inventory_adjustments: list) -> 'ProductListAdjustInventory':
		"""
		Set Inventory_Adjustments.

		:param inventory_adjustments: {ProductInventoryAdjustment[]}
		:raises Exception:
		:returns: ProductListAdjustInventory
		"""

		for e in inventory_adjustments:
			if not isinstance(e, merchantapi.model.ProductInventoryAdjustment):
				raise Exception("")
		self.inventory_adjustments = inventory_adjustments
		return self
	
	def add_inventory_adjustment(self, inventory_adjustment) -> 'ProductListAdjustInventory':
		"""
		Add Inventory_Adjustments.

		:param inventory_adjustment: ProductInventoryAdjustment 
		:raises Exception:
		:returns: {ProductListAdjustInventory}
		"""

		if isinstance(inventory_adjustment, merchantapi.model.ProductInventoryAdjustment):
			self.inventory_adjustments.append(inventory_adjustment)
		elif isinstance(inventory_adjustment, dict):
			self.inventory_adjustments.append(merchantapi.model.ProductInventoryAdjustment(inventory_adjustment))
		else:
			raise Exception('Expected instance of ProductInventoryAdjustment or dict')
		return self

	def add_inventory_adjustments(self, inventory_adjustments: list) -> 'ProductListAdjustInventory':
		"""
		Add many ProductInventoryAdjustment.

		:param inventory_adjustments: List of ProductInventoryAdjustment
		:raises Exception:
		:returns: ProductListAdjustInventory
		"""

		for e in inventory_adjustments:
			if not isinstance(e, merchantapi.model.ProductInventoryAdjustment):
				raise Exception('')
			self.inventory_adjustments.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductListAdjustInventory':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductListAdjustInventory':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductListAdjustInventory(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if len(self.inventory_adjustments):
			data['Inventory_Adjustments'] = []

			for f in self.inventory_adjustments:
				data['Inventory_Adjustments'].append(f.to_dict())
		return data
