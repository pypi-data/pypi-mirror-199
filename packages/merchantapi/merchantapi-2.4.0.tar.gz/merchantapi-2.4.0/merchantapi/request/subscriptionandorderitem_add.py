"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request SubscriptionAndOrderItem_Add. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/subscriptionandorderitem_add
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class SubscriptionAndOrderItemAdd(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		SubscriptionAndOrderItemAdd Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.order_id = None
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.address_id = None
		self.customer_address_id = None
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.product_subscription_term_id = None
		self.product_subscription_term_description = None
		self.quantity = None
		self.next_date = None
		self.payment_card_id = None
		self.ship_id = None
		self.ship_data = None
		self.attributes = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'SubscriptionAndOrderItem_Add'

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_edit_customer(self) -> str:
		"""
		Get Edit_Customer.

		:returns: str
		"""

		return self.edit_customer

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_address_id(self) -> int:
		"""
		Get Address_ID.

		:returns: int
		"""

		return self.address_id

	def get_customer_address_id(self) -> int:
		"""
		Get CustomerAddress_ID.

		:returns: int
		"""

		return self.customer_address_id

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_subscription_term_id(self) -> int:
		"""
		Get ProductSubscriptionTerm_ID.

		:returns: int
		"""

		return self.product_subscription_term_id

	def get_product_subscription_term_description(self) -> str:
		"""
		Get ProductSubscriptionTerm_Description.

		:returns: str
		"""

		return self.product_subscription_term_description

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def get_next_date(self) -> int:
		"""
		Get NextDate.

		:returns: int
		"""

		return self.next_date

	def get_payment_card_id(self) -> int:
		"""
		Get PaymentCard_ID.

		:returns: int
		"""

		return self.payment_card_id

	def get_ship_id(self) -> int:
		"""
		Get Ship_ID.

		:returns: int
		"""

		return self.ship_id

	def get_ship_data(self) -> str:
		"""
		Get Ship_Data.

		:returns: str
		"""

		return self.ship_data

	def get_attributes(self) -> list:
		"""
		Get Attributes.

		:returns: List of SubscriptionAttribute
		"""

		return self.attributes

	def set_order_id(self, order_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.order_id = order_id
		return self

	def set_customer_id(self, customer_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.customer_login = customer_login
		return self

	def set_address_id(self, address_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.address_id = address_id
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_product_id(self, product_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.product_code = product_code
		return self

	def set_product_subscription_term_id(self, product_subscription_term_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set ProductSubscriptionTerm_ID.

		:param product_subscription_term_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.product_subscription_term_id = product_subscription_term_id
		return self

	def set_product_subscription_term_description(self, product_subscription_term_description: str) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set ProductSubscriptionTerm_Description.

		:param product_subscription_term_description: str
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.product_subscription_term_description = product_subscription_term_description
		return self

	def set_quantity(self, quantity: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Quantity.

		:param quantity: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.quantity = quantity
		return self

	def set_next_date(self, next_date: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set NextDate.

		:param next_date: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.next_date = next_date
		return self

	def set_payment_card_id(self, payment_card_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set PaymentCard_ID.

		:param payment_card_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.payment_card_id = payment_card_id
		return self

	def set_ship_id(self, ship_id: int) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Ship_ID.

		:param ship_id: int
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.ship_id = ship_id
		return self

	def set_ship_data(self, ship_data: str) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Ship_Data.

		:param ship_data: str
		:returns: SubscriptionAndOrderItemAdd
		"""

		self.ship_data = ship_data
		return self

	def set_attributes(self, attributes: list) -> 'SubscriptionAndOrderItemAdd':
		"""
		Set Attributes.

		:param attributes: {SubscriptionAttribute[]}
		:raises Exception:
		:returns: SubscriptionAndOrderItemAdd
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.SubscriptionAttribute):
				raise Exception("")
		self.attributes = attributes
		return self
	
	def add_attribute(self, attribute) -> 'SubscriptionAndOrderItemAdd':
		"""
		Add Attributes.

		:param attribute: SubscriptionAttribute 
		:raises Exception:
		:returns: {SubscriptionAndOrderItemAdd}
		"""

		if isinstance(attribute, merchantapi.model.SubscriptionAttribute):
			self.attributes.append(attribute)
		elif isinstance(attribute, dict):
			self.attributes.append(merchantapi.model.SubscriptionAttribute(attribute))
		else:
			raise Exception('Expected instance of SubscriptionAttribute or dict')
		return self

	def add_attributes(self, attributes: list) -> 'SubscriptionAndOrderItemAdd':
		"""
		Add many SubscriptionAttribute.

		:param attributes: List of SubscriptionAttribute
		:raises Exception:
		:returns: SubscriptionAndOrderItemAdd
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.SubscriptionAttribute):
				raise Exception('')
			self.attributes.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.SubscriptionAndOrderItemAdd':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'SubscriptionAndOrderItemAdd':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.SubscriptionAndOrderItemAdd(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.order_id is not None:
			data['Order_ID'] = self.order_id

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code

		if self.product_subscription_term_id is not None:
			data['ProductSubscriptionTerm_ID'] = self.product_subscription_term_id
		elif self.product_subscription_term_description is not None:
			data['ProductSubscriptionTerm_Description'] = self.product_subscription_term_description

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.address_id is not None:
			data['Address_ID'] = self.address_id
		elif self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id

		data['Quantity'] = self.quantity
		data['NextDate'] = self.next_date
		if self.payment_card_id is not None:
			data['PaymentCard_ID'] = self.payment_card_id
		if self.ship_id is not None:
			data['Ship_ID'] = self.ship_id
		if self.ship_data is not None:
			data['Ship_Data'] = self.ship_data
		if len(self.attributes):
			data['Attributes'] = []

			for f in self.attributes:
				data['Attributes'].append(f.to_dict())
		return data
