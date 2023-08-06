"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroup_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegroup_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, price_group: merchantapi.model.PriceGroup = None):
		"""
		PriceGroupUpdate Constructor.

		:param client: Client
		:param price_group: PriceGroup
		"""

		super().__init__(client)
		self.price_group_id = None
		self.edit_price_group = None
		self.price_group_name = None
		self.name = None
		self.customer_scope = None
		self.rate = None
		self.discount = None
		self.markup = None
		self.module_id = None
		self.exclusion = None
		self.description = None
		self.display = None
		self.date_time_start = None
		self.date_time_end = None
		self.qualifying_min_subtotal = None
		self.qualifying_max_subtotal = None
		self.qualifying_min_quantity = None
		self.qualifying_max_quantity = None
		self.qualifying_min_weight = None
		self.qualifying_max_weight = None
		self.basket_min_subtotal = None
		self.basket_max_subtotal = None
		self.basket_min_quantity = None
		self.basket_max_quantity = None
		self.basket_min_weight = None
		self.basket_max_weight = None
		self.priority = None
		self.exclusions = []
		self.module_fields = {}
		if isinstance(price_group, merchantapi.model.PriceGroup):
			if price_group.get_id():
				self.set_price_group_id(price_group.get_id())

			self.set_price_group_name(price_group.get_name())
			self.set_name(price_group.get_name())
			self.set_customer_scope(price_group.get_customer_scope())
			self.set_rate(price_group.get_rate())
			self.set_discount(price_group.get_discount())
			self.set_markup(price_group.get_markup())
			self.set_exclusion(price_group.get_exclusion())
			self.set_description(price_group.get_description())
			self.set_display(price_group.get_display())
			self.set_date_time_start(price_group.get_date_time_start())
			self.set_date_time_end(price_group.get_date_time_end())
			self.set_qualifying_min_subtotal(price_group.get_minimum_subtotal())
			self.set_qualifying_max_subtotal(price_group.get_maximum_subtotal())
			self.set_qualifying_min_quantity(price_group.get_minimum_quantity())
			self.set_qualifying_max_quantity(price_group.get_maximum_quantity())
			self.set_qualifying_min_weight(price_group.get_minimum_weight())
			self.set_qualifying_max_weight(price_group.get_maximum_weight())
			self.set_basket_min_subtotal(price_group.get_basket_minimum_subtotal())
			self.set_basket_max_subtotal(price_group.get_basket_maximum_subtotal())
			self.set_basket_min_quantity(price_group.get_basket_minimum_quantity())
			self.set_basket_max_quantity(price_group.get_basket_maximum_quantity())
			self.set_basket_min_weight(price_group.get_basket_minimum_weight())
			self.set_basket_max_weight(price_group.get_basket_maximum_weight())
			self.set_priority(price_group.get_priority())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroup_Update'

	def get_price_group_id(self) -> int:
		"""
		Get PriceGroup_ID.

		:returns: int
		"""

		return self.price_group_id

	def get_edit_price_group(self) -> str:
		"""
		Get Edit_PriceGroup.

		:returns: str
		"""

		return self.edit_price_group

	def get_price_group_name(self) -> str:
		"""
		Get PriceGroup_Name.

		:returns: str
		"""

		return self.price_group_name

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_customer_scope(self) -> str:
		"""
		Get CustomerScope.

		:returns: str
		"""

		return self.customer_scope

	def get_rate(self) -> str:
		"""
		Get Rate.

		:returns: str
		"""

		return self.rate

	def get_discount(self) -> float:
		"""
		Get Discount.

		:returns: float
		"""

		return self.discount

	def get_markup(self) -> float:
		"""
		Get Markup.

		:returns: float
		"""

		return self.markup

	def get_module_id(self) -> int:
		"""
		Get Module_ID.

		:returns: int
		"""

		return self.module_id

	def get_exclusion(self) -> bool:
		"""
		Get Exclusion.

		:returns: bool
		"""

		return self.exclusion

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_display(self) -> bool:
		"""
		Get Display.

		:returns: bool
		"""

		return self.display

	def get_date_time_start(self) -> int:
		"""
		Get DateTime_Start.

		:returns: int
		"""

		return self.date_time_start

	def get_date_time_end(self) -> int:
		"""
		Get DateTime_End.

		:returns: int
		"""

		return self.date_time_end

	def get_qualifying_min_subtotal(self) -> float:
		"""
		Get Qualifying_Min_Subtotal.

		:returns: float
		"""

		return self.qualifying_min_subtotal

	def get_qualifying_max_subtotal(self) -> float:
		"""
		Get Qualifying_Max_Subtotal.

		:returns: float
		"""

		return self.qualifying_max_subtotal

	def get_qualifying_min_quantity(self) -> int:
		"""
		Get Qualifying_Min_Quantity.

		:returns: int
		"""

		return self.qualifying_min_quantity

	def get_qualifying_max_quantity(self) -> int:
		"""
		Get Qualifying_Max_Quantity.

		:returns: int
		"""

		return self.qualifying_max_quantity

	def get_qualifying_min_weight(self) -> float:
		"""
		Get Qualifying_Min_Weight.

		:returns: float
		"""

		return self.qualifying_min_weight

	def get_qualifying_max_weight(self) -> float:
		"""
		Get Qualifying_Max_Weight.

		:returns: float
		"""

		return self.qualifying_max_weight

	def get_basket_min_subtotal(self) -> float:
		"""
		Get Basket_Min_Subtotal.

		:returns: float
		"""

		return self.basket_min_subtotal

	def get_basket_max_subtotal(self) -> float:
		"""
		Get Basket_Max_Subtotal.

		:returns: float
		"""

		return self.basket_max_subtotal

	def get_basket_min_quantity(self) -> int:
		"""
		Get Basket_Min_Quantity.

		:returns: int
		"""

		return self.basket_min_quantity

	def get_basket_max_quantity(self) -> int:
		"""
		Get Basket_Max_Quantity.

		:returns: int
		"""

		return self.basket_max_quantity

	def get_basket_min_weight(self) -> float:
		"""
		Get Basket_Min_Weight.

		:returns: float
		"""

		return self.basket_min_weight

	def get_basket_max_weight(self) -> float:
		"""
		Get Basket_Max_Weight.

		:returns: float
		"""

		return self.basket_max_weight

	def get_priority(self) -> int:
		"""
		Get Priority.

		:returns: int
		"""

		return self.priority

	def get_exclusions(self) -> list:
		"""
		Get Exclusions.

		:returns: List of PriceGroupExclusion
		"""

		return self.exclusions

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_price_group_id(self, price_group_id: int) -> 'PriceGroupUpdate':
		"""
		Set PriceGroup_ID.

		:param price_group_id: int
		:returns: PriceGroupUpdate
		"""

		self.price_group_id = price_group_id
		return self

	def set_edit_price_group(self, edit_price_group: str) -> 'PriceGroupUpdate':
		"""
		Set Edit_PriceGroup.

		:param edit_price_group: str
		:returns: PriceGroupUpdate
		"""

		self.edit_price_group = edit_price_group
		return self

	def set_price_group_name(self, price_group_name: str) -> 'PriceGroupUpdate':
		"""
		Set PriceGroup_Name.

		:param price_group_name: str
		:returns: PriceGroupUpdate
		"""

		self.price_group_name = price_group_name
		return self

	def set_name(self, name: str) -> 'PriceGroupUpdate':
		"""
		Set Name.

		:param name: str
		:returns: PriceGroupUpdate
		"""

		self.name = name
		return self

	def set_customer_scope(self, customer_scope: str) -> 'PriceGroupUpdate':
		"""
		Set CustomerScope.

		:param customer_scope: str
		:returns: PriceGroupUpdate
		"""

		self.customer_scope = customer_scope
		return self

	def set_rate(self, rate: str) -> 'PriceGroupUpdate':
		"""
		Set Rate.

		:param rate: str
		:returns: PriceGroupUpdate
		"""

		self.rate = rate
		return self

	def set_discount(self, discount: float) -> 'PriceGroupUpdate':
		"""
		Set Discount.

		:param discount: float
		:returns: PriceGroupUpdate
		"""

		self.discount = discount
		return self

	def set_markup(self, markup: float) -> 'PriceGroupUpdate':
		"""
		Set Markup.

		:param markup: float
		:returns: PriceGroupUpdate
		"""

		self.markup = markup
		return self

	def set_module_id(self, module_id: int) -> 'PriceGroupUpdate':
		"""
		Set Module_ID.

		:param module_id: int
		:returns: PriceGroupUpdate
		"""

		self.module_id = module_id
		return self

	def set_exclusion(self, exclusion: bool) -> 'PriceGroupUpdate':
		"""
		Set Exclusion.

		:param exclusion: bool
		:returns: PriceGroupUpdate
		"""

		self.exclusion = exclusion
		return self

	def set_description(self, description: str) -> 'PriceGroupUpdate':
		"""
		Set Description.

		:param description: str
		:returns: PriceGroupUpdate
		"""

		self.description = description
		return self

	def set_display(self, display: bool) -> 'PriceGroupUpdate':
		"""
		Set Display.

		:param display: bool
		:returns: PriceGroupUpdate
		"""

		self.display = display
		return self

	def set_date_time_start(self, date_time_start: int) -> 'PriceGroupUpdate':
		"""
		Set DateTime_Start.

		:param date_time_start: int
		:returns: PriceGroupUpdate
		"""

		self.date_time_start = date_time_start
		return self

	def set_date_time_end(self, date_time_end: int) -> 'PriceGroupUpdate':
		"""
		Set DateTime_End.

		:param date_time_end: int
		:returns: PriceGroupUpdate
		"""

		self.date_time_end = date_time_end
		return self

	def set_qualifying_min_subtotal(self, qualifying_min_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Min_Subtotal.

		:param qualifying_min_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_min_subtotal = qualifying_min_subtotal
		return self

	def set_qualifying_max_subtotal(self, qualifying_max_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Max_Subtotal.

		:param qualifying_max_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_max_subtotal = qualifying_max_subtotal
		return self

	def set_qualifying_min_quantity(self, qualifying_min_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Min_Quantity.

		:param qualifying_min_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.qualifying_min_quantity = qualifying_min_quantity
		return self

	def set_qualifying_max_quantity(self, qualifying_max_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Max_Quantity.

		:param qualifying_max_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.qualifying_max_quantity = qualifying_max_quantity
		return self

	def set_qualifying_min_weight(self, qualifying_min_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Min_Weight.

		:param qualifying_min_weight: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_min_weight = qualifying_min_weight
		return self

	def set_qualifying_max_weight(self, qualifying_max_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Qualifying_Max_Weight.

		:param qualifying_max_weight: float
		:returns: PriceGroupUpdate
		"""

		self.qualifying_max_weight = qualifying_max_weight
		return self

	def set_basket_min_subtotal(self, basket_min_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Min_Subtotal.

		:param basket_min_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.basket_min_subtotal = basket_min_subtotal
		return self

	def set_basket_max_subtotal(self, basket_max_subtotal: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Max_Subtotal.

		:param basket_max_subtotal: float
		:returns: PriceGroupUpdate
		"""

		self.basket_max_subtotal = basket_max_subtotal
		return self

	def set_basket_min_quantity(self, basket_min_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Basket_Min_Quantity.

		:param basket_min_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.basket_min_quantity = basket_min_quantity
		return self

	def set_basket_max_quantity(self, basket_max_quantity: int) -> 'PriceGroupUpdate':
		"""
		Set Basket_Max_Quantity.

		:param basket_max_quantity: int
		:returns: PriceGroupUpdate
		"""

		self.basket_max_quantity = basket_max_quantity
		return self

	def set_basket_min_weight(self, basket_min_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Min_Weight.

		:param basket_min_weight: float
		:returns: PriceGroupUpdate
		"""

		self.basket_min_weight = basket_min_weight
		return self

	def set_basket_max_weight(self, basket_max_weight: float) -> 'PriceGroupUpdate':
		"""
		Set Basket_Max_Weight.

		:param basket_max_weight: float
		:returns: PriceGroupUpdate
		"""

		self.basket_max_weight = basket_max_weight
		return self

	def set_priority(self, priority: int) -> 'PriceGroupUpdate':
		"""
		Set Priority.

		:param priority: int
		:returns: PriceGroupUpdate
		"""

		self.priority = priority
		return self

	def set_exclusions(self, exclusions: list) -> 'PriceGroupUpdate':
		"""
		Set Exclusions.

		:param exclusions: {PriceGroupExclusion[]}
		:raises Exception:
		:returns: PriceGroupUpdate
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.PriceGroupExclusion):
				raise Exception("")
		self.exclusions = exclusions
		return self

	def set_module_fields(self, module_fields) -> 'PriceGroupUpdate':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: PriceGroupUpdate
		"""

		self.module_fields = module_fields
		return self
	
	def add_price_group_exclusion(self, price_group_exclusion) -> 'PriceGroupUpdate':
		"""
		Add Exclusions.

		:param price_group_exclusion: PriceGroupExclusion 
		:raises Exception:
		:returns: {PriceGroupUpdate}
		"""

		if isinstance(price_group_exclusion, merchantapi.model.PriceGroupExclusion):
			self.exclusions.append(price_group_exclusion)
		elif isinstance(price_group_exclusion, dict):
			self.exclusions.append(merchantapi.model.PriceGroupExclusion(price_group_exclusion))
		else:
			raise Exception('Expected instance of PriceGroupExclusion or dict')
		return self

	def add_exclusions(self, exclusions: list) -> 'PriceGroupUpdate':
		"""
		Add many PriceGroupExclusion.

		:param exclusions: List of PriceGroupExclusion
		:raises Exception:
		:returns: PriceGroupUpdate
		"""

		for e in exclusions:
			if not isinstance(e, merchantapi.model.PriceGroupExclusion):
				raise Exception('')
			self.exclusions.append(e)

		return self

	def set_module_field(self, field: str, value) -> 'PriceGroupUpdate':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {PriceGroupUpdate}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		if self.price_group_id is not None:
			data['PriceGroup_ID'] = self.price_group_id
		elif self.edit_price_group is not None:
			data['Edit_PriceGroup'] = self.edit_price_group
		elif self.price_group_name is not None:
			data['PriceGroup_Name'] = self.price_group_name

		data['PriceGroup_Name'] = self.price_group_name
		if self.name is not None:
			data['Name'] = self.name
		if self.customer_scope is not None:
			data['CustomerScope'] = self.customer_scope
		if self.rate is not None:
			data['Rate'] = self.rate
		if self.discount is not None:
			data['Discount'] = self.discount
		if self.markup is not None:
			data['Markup'] = self.markup
		if self.module_id is not None:
			data['Module_ID'] = self.module_id
		if self.exclusion is not None:
			data['Exclusion'] = self.exclusion
		if self.description is not None:
			data['Description'] = self.description
		if self.display is not None:
			data['Display'] = self.display
		if self.date_time_start is not None:
			data['DateTime_Start'] = self.date_time_start
		if self.date_time_end is not None:
			data['DateTime_End'] = self.date_time_end
		if self.qualifying_min_subtotal is not None:
			data['Qualifying_Min_Subtotal'] = self.qualifying_min_subtotal
		if self.qualifying_max_subtotal is not None:
			data['Qualifying_Max_Subtotal'] = self.qualifying_max_subtotal
		if self.qualifying_min_quantity is not None:
			data['Qualifying_Min_Quantity'] = self.qualifying_min_quantity
		if self.qualifying_max_quantity is not None:
			data['Qualifying_Max_Quantity'] = self.qualifying_max_quantity
		if self.qualifying_min_weight is not None:
			data['Qualifying_Min_Weight'] = self.qualifying_min_weight
		if self.qualifying_max_weight is not None:
			data['Qualifying_Max_Weight'] = self.qualifying_max_weight
		if self.basket_min_subtotal is not None:
			data['Basket_Min_Subtotal'] = self.basket_min_subtotal
		if self.basket_max_subtotal is not None:
			data['Basket_Max_Subtotal'] = self.basket_max_subtotal
		if self.basket_min_quantity is not None:
			data['Basket_Min_Quantity'] = self.basket_min_quantity
		if self.basket_max_quantity is not None:
			data['Basket_Max_Quantity'] = self.basket_max_quantity
		if self.basket_min_weight is not None:
			data['Basket_Min_Weight'] = self.basket_min_weight
		if self.basket_max_weight is not None:
			data['Basket_Max_Weight'] = self.basket_max_weight
		if self.priority is not None:
			data['Priority'] = self.priority
		if len(self.exclusions):
			data['Exclusions'] = []

			for f in self.exclusions:
				data['Exclusions'].append(f.to_dict())
		return data
