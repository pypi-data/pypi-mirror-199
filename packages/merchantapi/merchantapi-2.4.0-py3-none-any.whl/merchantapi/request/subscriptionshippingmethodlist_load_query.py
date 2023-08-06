"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request SubscriptionShippingMethodList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/subscriptionshippingmethodlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class SubscriptionShippingMethodListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'method',
		'price'
	]

	available_sort_fields = [
		'method',
		'price'
	]

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		SubscriptionShippingMethodListLoadQuery Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.product_subscription_term_id = None
		self.product_subscription_term_description = None
		self.customer_address_id = None
		self.address_id = None
		self.payment_card_id = None
		self.customer_payment_card_id = None
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.attributes = []
		self.quantity = None
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

		return 'SubscriptionShippingMethodList_Load_Query'

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

	def get_customer_address_id(self) -> int:
		"""
		Get CustomerAddress_ID.

		:returns: int
		"""

		return self.customer_address_id

	def get_address_id(self) -> int:
		"""
		Get Address_ID.

		:returns: int
		"""

		return self.address_id

	def get_payment_card_id(self) -> int:
		"""
		Get PaymentCard_ID.

		:returns: int
		"""

		return self.payment_card_id

	def get_customer_payment_card_id(self) -> int:
		"""
		Get CustomerPaymentCard_ID.

		:returns: int
		"""

		return self.customer_payment_card_id

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

	def get_attributes(self) -> list:
		"""
		Get Attributes.

		:returns: List of SubscriptionAttribute
		"""

		return self.attributes

	def get_quantity(self) -> int:
		"""
		Get Quantity.

		:returns: int
		"""

		return self.quantity

	def set_product_id(self, product_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.product_code = product_code
		return self

	def set_product_subscription_term_id(self, product_subscription_term_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set ProductSubscriptionTerm_ID.

		:param product_subscription_term_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.product_subscription_term_id = product_subscription_term_id
		return self

	def set_product_subscription_term_description(self, product_subscription_term_description: str) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set ProductSubscriptionTerm_Description.

		:param product_subscription_term_description: str
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.product_subscription_term_description = product_subscription_term_description
		return self

	def set_customer_address_id(self, customer_address_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set CustomerAddress_ID.

		:param customer_address_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.customer_address_id = customer_address_id
		return self

	def set_address_id(self, address_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Address_ID.

		:param address_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.address_id = address_id
		return self

	def set_payment_card_id(self, payment_card_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set PaymentCard_ID.

		:param payment_card_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.payment_card_id = payment_card_id
		return self

	def set_customer_payment_card_id(self, customer_payment_card_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set CustomerPaymentCard_ID.

		:param customer_payment_card_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.customer_payment_card_id = customer_payment_card_id
		return self

	def set_customer_id(self, customer_id: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	def set_attributes(self, attributes: list) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Attributes.

		:param attributes: {SubscriptionAttribute[]}
		:raises Exception:
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.SubscriptionAttribute):
				raise Exception("")
		self.attributes = attributes
		return self

	def set_quantity(self, quantity: int) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Set Quantity.

		:param quantity: int
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		self.quantity = quantity
		return self
	
	def add_subscription_attribute(self, subscription_attribute) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Add Attributes.

		:param subscription_attribute: SubscriptionAttribute 
		:raises Exception:
		:returns: {SubscriptionShippingMethodListLoadQuery}
		"""

		if isinstance(subscription_attribute, merchantapi.model.SubscriptionAttribute):
			self.attributes.append(subscription_attribute)
		elif isinstance(subscription_attribute, dict):
			self.attributes.append(merchantapi.model.SubscriptionAttribute(subscription_attribute))
		else:
			raise Exception('Expected instance of SubscriptionAttribute or dict')
		return self

	def add_attributes(self, attributes: list) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Add many SubscriptionAttribute.

		:param attributes: List of SubscriptionAttribute
		:raises Exception:
		:returns: SubscriptionShippingMethodListLoadQuery
		"""

		for e in attributes:
			if not isinstance(e, merchantapi.model.SubscriptionAttribute):
				raise Exception('')
			self.attributes.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.SubscriptionShippingMethodListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'SubscriptionShippingMethodListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.SubscriptionShippingMethodListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

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

		if self.customer_address_id is not None:
			data['CustomerAddress_ID'] = self.customer_address_id
		elif self.address_id is not None:
			data['Address_ID'] = self.address_id

		if self.payment_card_id is not None:
			data['PaymentCard_ID'] = self.payment_card_id
		elif self.customer_payment_card_id is not None:
			data['CustomerPaymentCard_ID'] = self.customer_payment_card_id

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if len(self.attributes):
			data['Attributes'] = []

			for f in self.attributes:
				data['Attributes'].append(f.to_dict())
		data['Quantity'] = self.quantity
		return data
