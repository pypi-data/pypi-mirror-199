"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request InventoryProductSettings_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/inventoryproductsettings_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class InventoryProductSettingsUpdate(merchantapi.abstract.Request):
	# INVENTORY_CHOICE constants.
	INVENTORY_CHOICE_DEFAULT = 'Default'
	INVENTORY_CHOICE_YES = 'Yes'
	INVENTORY_CHOICE_NO = 'No'

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		InventoryProductSettingsUpdate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.track_low_stock_level = None
		self.track_out_of_stock_level = None
		self.hide_out_of_stock_products = None
		self.low_stock_level = None
		self.out_of_stock_level = None
		self.track_product = None
		self.in_stock_message_short = None
		self.in_stock_message_long = None
		self.low_stock_message_short = None
		self.low_stock_message_long = None
		self.out_of_stock_message_short = None
		self.out_of_stock_message_long = None
		self.limited_stock_message = None
		self.adjust_stock_by = None
		self.current_stock = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'InventoryProductSettings_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_track_low_stock_level(self) -> str:
		"""
		Get TrackLowStockLevel.

		:returns: str
		"""

		return self.track_low_stock_level

	def get_track_out_of_stock_level(self) -> str:
		"""
		Get TrackOutOfStockLevel.

		:returns: str
		"""

		return self.track_out_of_stock_level

	def get_hide_out_of_stock_products(self) -> str:
		"""
		Get HideOutOfStockProducts.

		:returns: str
		"""

		return self.hide_out_of_stock_products

	def get_low_stock_level(self) -> int:
		"""
		Get LowStockLevel.

		:returns: int
		"""

		return self.low_stock_level

	def get_out_of_stock_level(self) -> int:
		"""
		Get OutOfStockLevel.

		:returns: int
		"""

		return self.out_of_stock_level

	def get_track_product(self) -> bool:
		"""
		Get TrackProduct.

		:returns: bool
		"""

		return self.track_product

	def get_in_stock_message_short(self) -> str:
		"""
		Get InStockMessageShort.

		:returns: str
		"""

		return self.in_stock_message_short

	def get_in_stock_message_long(self) -> str:
		"""
		Get InStockMessageLong.

		:returns: str
		"""

		return self.in_stock_message_long

	def get_low_stock_message_short(self) -> str:
		"""
		Get LowStockMessageShort.

		:returns: str
		"""

		return self.low_stock_message_short

	def get_low_stock_message_long(self) -> str:
		"""
		Get LowStockMessageLong.

		:returns: str
		"""

		return self.low_stock_message_long

	def get_out_of_stock_message_short(self) -> str:
		"""
		Get OutOfStockMessageShort.

		:returns: str
		"""

		return self.out_of_stock_message_short

	def get_out_of_stock_message_long(self) -> str:
		"""
		Get OutOfStockMessageLong.

		:returns: str
		"""

		return self.out_of_stock_message_long

	def get_limited_stock_message(self) -> str:
		"""
		Get LimitedStockMessage.

		:returns: str
		"""

		return self.limited_stock_message

	def get_adjust_stock_by(self) -> int:
		"""
		Get AdjustStockBy.

		:returns: int
		"""

		return self.adjust_stock_by

	def get_current_stock(self) -> int:
		"""
		Get CurrentStock.

		:returns: int
		"""

		return self.current_stock

	def set_product_id(self, product_id: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_track_low_stock_level(self, track_low_stock_level: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set TrackLowStockLevel.

		:param track_low_stock_level: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.track_low_stock_level = track_low_stock_level
		return self

	def set_track_out_of_stock_level(self, track_out_of_stock_level: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set TrackOutOfStockLevel.

		:param track_out_of_stock_level: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.track_out_of_stock_level = track_out_of_stock_level
		return self

	def set_hide_out_of_stock_products(self, hide_out_of_stock_products: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set HideOutOfStockProducts.

		:param hide_out_of_stock_products: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.hide_out_of_stock_products = hide_out_of_stock_products
		return self

	def set_low_stock_level(self, low_stock_level: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set LowStockLevel.

		:param low_stock_level: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.low_stock_level = low_stock_level
		return self

	def set_out_of_stock_level(self, out_of_stock_level: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set OutOfStockLevel.

		:param out_of_stock_level: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.out_of_stock_level = out_of_stock_level
		return self

	def set_track_product(self, track_product: bool) -> 'InventoryProductSettingsUpdate':
		"""
		Set TrackProduct.

		:param track_product: bool
		:returns: InventoryProductSettingsUpdate
		"""

		self.track_product = track_product
		return self

	def set_in_stock_message_short(self, in_stock_message_short: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set InStockMessageShort.

		:param in_stock_message_short: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.in_stock_message_short = in_stock_message_short
		return self

	def set_in_stock_message_long(self, in_stock_message_long: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set InStockMessageLong.

		:param in_stock_message_long: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.in_stock_message_long = in_stock_message_long
		return self

	def set_low_stock_message_short(self, low_stock_message_short: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set LowStockMessageShort.

		:param low_stock_message_short: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.low_stock_message_short = low_stock_message_short
		return self

	def set_low_stock_message_long(self, low_stock_message_long: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set LowStockMessageLong.

		:param low_stock_message_long: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.low_stock_message_long = low_stock_message_long
		return self

	def set_out_of_stock_message_short(self, out_of_stock_message_short: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set OutOfStockMessageShort.

		:param out_of_stock_message_short: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.out_of_stock_message_short = out_of_stock_message_short
		return self

	def set_out_of_stock_message_long(self, out_of_stock_message_long: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set OutOfStockMessageLong.

		:param out_of_stock_message_long: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.out_of_stock_message_long = out_of_stock_message_long
		return self

	def set_limited_stock_message(self, limited_stock_message: str) -> 'InventoryProductSettingsUpdate':
		"""
		Set LimitedStockMessage.

		:param limited_stock_message: str
		:returns: InventoryProductSettingsUpdate
		"""

		self.limited_stock_message = limited_stock_message
		return self

	def set_adjust_stock_by(self, adjust_stock_by: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set AdjustStockBy.

		:param adjust_stock_by: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.adjust_stock_by = adjust_stock_by
		return self

	def set_current_stock(self, current_stock: int) -> 'InventoryProductSettingsUpdate':
		"""
		Set CurrentStock.

		:param current_stock: int
		:returns: InventoryProductSettingsUpdate
		"""

		self.current_stock = current_stock
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.InventoryProductSettingsUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'InventoryProductSettingsUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.InventoryProductSettingsUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product

		if self.track_low_stock_level is not None:
			data['TrackLowStockLevel'] = self.track_low_stock_level
		if self.track_out_of_stock_level is not None:
			data['TrackOutOfStockLevel'] = self.track_out_of_stock_level
		if self.hide_out_of_stock_products is not None:
			data['HideOutOfStockProducts'] = self.hide_out_of_stock_products
		if self.low_stock_level is not None:
			data['LowStockLevel'] = self.low_stock_level
		if self.out_of_stock_level is not None:
			data['OutOfStockLevel'] = self.out_of_stock_level
		if self.track_product is not None:
			data['TrackProduct'] = self.track_product
		if self.in_stock_message_short is not None:
			data['InStockMessageShort'] = self.in_stock_message_short
		if self.in_stock_message_long is not None:
			data['InStockMessageLong'] = self.in_stock_message_long
		if self.low_stock_message_short is not None:
			data['LowStockMessageShort'] = self.low_stock_message_short
		if self.low_stock_message_long is not None:
			data['LowStockMessageLong'] = self.low_stock_message_long
		if self.out_of_stock_message_short is not None:
			data['OutOfStockMessageShort'] = self.out_of_stock_message_short
		if self.out_of_stock_message_long is not None:
			data['OutOfStockMessageLong'] = self.out_of_stock_message_long
		if self.limited_stock_message is not None:
			data['LimitedStockMessage'] = self.limited_stock_message
		if self.adjust_stock_by is not None:
			data['AdjustStockBy'] = self.adjust_stock_by
		if self.current_stock is not None:
			data['CurrentStock'] = self.current_stock
		return data
