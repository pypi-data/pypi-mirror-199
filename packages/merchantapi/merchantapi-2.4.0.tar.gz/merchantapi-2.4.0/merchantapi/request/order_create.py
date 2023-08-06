"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Order_Create. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_create
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderCreate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		OrderCreate Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_login = None
		self.customer_id = None
		self.ship_first_name = None
		self.ship_last_name = None
		self.ship_email = None
		self.ship_phone = None
		self.ship_fax = None
		self.ship_company = None
		self.ship_address1 = None
		self.ship_address2 = None
		self.ship_city = None
		self.ship_state = None
		self.ship_zip = None
		self.ship_country = None
		self.ship_residential = None
		self.bill_first_name = None
		self.bill_last_name = None
		self.bill_email = None
		self.bill_phone = None
		self.bill_fax = None
		self.bill_company = None
		self.bill_address1 = None
		self.bill_address2 = None
		self.bill_city = None
		self.bill_state = None
		self.bill_zip = None
		self.bill_country = None
		self.items = []
		self.products = []
		self.charges = []
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		self.shipping_module_code = None
		self.shipping_module_data = None
		self.calculate_charges = None
		self.trigger_fulfillment_modules = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_customer_login(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Create'

	def get_customer_login(self) -> str:
		"""
		Get Customer_Login.

		:returns: str
		"""

		return self.customer_login

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_ship_first_name(self) -> str:
		"""
		Get ShipFirstName.

		:returns: str
		"""

		return self.ship_first_name

	def get_ship_last_name(self) -> str:
		"""
		Get ShipLastName.

		:returns: str
		"""

		return self.ship_last_name

	def get_ship_email(self) -> str:
		"""
		Get ShipEmail.

		:returns: str
		"""

		return self.ship_email

	def get_ship_phone(self) -> str:
		"""
		Get ShipPhone.

		:returns: str
		"""

		return self.ship_phone

	def get_ship_fax(self) -> str:
		"""
		Get ShipFax.

		:returns: str
		"""

		return self.ship_fax

	def get_ship_company(self) -> str:
		"""
		Get ShipCompany.

		:returns: str
		"""

		return self.ship_company

	def get_ship_address1(self) -> str:
		"""
		Get ShipAddress1.

		:returns: str
		"""

		return self.ship_address1

	def get_ship_address2(self) -> str:
		"""
		Get ShipAddress2.

		:returns: str
		"""

		return self.ship_address2

	def get_ship_city(self) -> str:
		"""
		Get ShipCity.

		:returns: str
		"""

		return self.ship_city

	def get_ship_state(self) -> str:
		"""
		Get ShipState.

		:returns: str
		"""

		return self.ship_state

	def get_ship_zip(self) -> str:
		"""
		Get ShipZip.

		:returns: str
		"""

		return self.ship_zip

	def get_ship_country(self) -> str:
		"""
		Get ShipCountry.

		:returns: str
		"""

		return self.ship_country

	def get_ship_residential(self) -> bool:
		"""
		Get ShipResidential.

		:returns: bool
		"""

		return self.ship_residential

	def get_bill_first_name(self) -> str:
		"""
		Get BillFirstName.

		:returns: str
		"""

		return self.bill_first_name

	def get_bill_last_name(self) -> str:
		"""
		Get BillLastName.

		:returns: str
		"""

		return self.bill_last_name

	def get_bill_email(self) -> str:
		"""
		Get BillEmail.

		:returns: str
		"""

		return self.bill_email

	def get_bill_phone(self) -> str:
		"""
		Get BillPhone.

		:returns: str
		"""

		return self.bill_phone

	def get_bill_fax(self) -> str:
		"""
		Get BillFax.

		:returns: str
		"""

		return self.bill_fax

	def get_bill_company(self) -> str:
		"""
		Get BillCompany.

		:returns: str
		"""

		return self.bill_company

	def get_bill_address1(self) -> str:
		"""
		Get BillAddress1.

		:returns: str
		"""

		return self.bill_address1

	def get_bill_address2(self) -> str:
		"""
		Get BillAddress2.

		:returns: str
		"""

		return self.bill_address2

	def get_bill_city(self) -> str:
		"""
		Get BillCity.

		:returns: str
		"""

		return self.bill_city

	def get_bill_state(self) -> str:
		"""
		Get BillState.

		:returns: str
		"""

		return self.bill_state

	def get_bill_zip(self) -> str:
		"""
		Get BillZip.

		:returns: str
		"""

		return self.bill_zip

	def get_bill_country(self) -> str:
		"""
		Get BillCountry.

		:returns: str
		"""

		return self.bill_country

	def get_items(self) -> list:
		"""
		Get Items.

		:returns: List of OrderItem
		"""

		return self.items

	def get_products(self) -> list:
		"""
		Get Products.

		:returns: List of OrderProduct
		"""

		return self.products

	def get_charges(self) -> list:
		"""
		Get Charges.

		:returns: List of OrderCharge
		"""

		return self.charges

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def get_shipping_module_code(self) -> str:
		"""
		Get Shipping_Module_Code.

		:returns: str
		"""

		return self.shipping_module_code

	def get_shipping_module_data(self) -> str:
		"""
		Get Shipping_Module_Data.

		:returns: str
		"""

		return self.shipping_module_data

	def get_calculate_charges(self) -> bool:
		"""
		Get CalculateCharges.

		:returns: bool
		"""

		return self.calculate_charges

	def get_trigger_fulfillment_modules(self) -> bool:
		"""
		Get TriggerFulfillmentModules.

		:returns: bool
		"""

		return self.trigger_fulfillment_modules

	def set_customer_login(self, customer_login: str) -> 'OrderCreate':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: OrderCreate
		"""

		self.customer_login = customer_login
		return self

	def set_customer_id(self, customer_id: int) -> 'OrderCreate':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OrderCreate
		"""

		self.customer_id = customer_id
		return self

	def set_ship_first_name(self, ship_first_name: str) -> 'OrderCreate':
		"""
		Set ShipFirstName.

		:param ship_first_name: str
		:returns: OrderCreate
		"""

		self.ship_first_name = ship_first_name
		return self

	def set_ship_last_name(self, ship_last_name: str) -> 'OrderCreate':
		"""
		Set ShipLastName.

		:param ship_last_name: str
		:returns: OrderCreate
		"""

		self.ship_last_name = ship_last_name
		return self

	def set_ship_email(self, ship_email: str) -> 'OrderCreate':
		"""
		Set ShipEmail.

		:param ship_email: str
		:returns: OrderCreate
		"""

		self.ship_email = ship_email
		return self

	def set_ship_phone(self, ship_phone: str) -> 'OrderCreate':
		"""
		Set ShipPhone.

		:param ship_phone: str
		:returns: OrderCreate
		"""

		self.ship_phone = ship_phone
		return self

	def set_ship_fax(self, ship_fax: str) -> 'OrderCreate':
		"""
		Set ShipFax.

		:param ship_fax: str
		:returns: OrderCreate
		"""

		self.ship_fax = ship_fax
		return self

	def set_ship_company(self, ship_company: str) -> 'OrderCreate':
		"""
		Set ShipCompany.

		:param ship_company: str
		:returns: OrderCreate
		"""

		self.ship_company = ship_company
		return self

	def set_ship_address1(self, ship_address1: str) -> 'OrderCreate':
		"""
		Set ShipAddress1.

		:param ship_address1: str
		:returns: OrderCreate
		"""

		self.ship_address1 = ship_address1
		return self

	def set_ship_address2(self, ship_address2: str) -> 'OrderCreate':
		"""
		Set ShipAddress2.

		:param ship_address2: str
		:returns: OrderCreate
		"""

		self.ship_address2 = ship_address2
		return self

	def set_ship_city(self, ship_city: str) -> 'OrderCreate':
		"""
		Set ShipCity.

		:param ship_city: str
		:returns: OrderCreate
		"""

		self.ship_city = ship_city
		return self

	def set_ship_state(self, ship_state: str) -> 'OrderCreate':
		"""
		Set ShipState.

		:param ship_state: str
		:returns: OrderCreate
		"""

		self.ship_state = ship_state
		return self

	def set_ship_zip(self, ship_zip: str) -> 'OrderCreate':
		"""
		Set ShipZip.

		:param ship_zip: str
		:returns: OrderCreate
		"""

		self.ship_zip = ship_zip
		return self

	def set_ship_country(self, ship_country: str) -> 'OrderCreate':
		"""
		Set ShipCountry.

		:param ship_country: str
		:returns: OrderCreate
		"""

		self.ship_country = ship_country
		return self

	def set_ship_residential(self, ship_residential: bool) -> 'OrderCreate':
		"""
		Set ShipResidential.

		:param ship_residential: bool
		:returns: OrderCreate
		"""

		self.ship_residential = ship_residential
		return self

	def set_bill_first_name(self, bill_first_name: str) -> 'OrderCreate':
		"""
		Set BillFirstName.

		:param bill_first_name: str
		:returns: OrderCreate
		"""

		self.bill_first_name = bill_first_name
		return self

	def set_bill_last_name(self, bill_last_name: str) -> 'OrderCreate':
		"""
		Set BillLastName.

		:param bill_last_name: str
		:returns: OrderCreate
		"""

		self.bill_last_name = bill_last_name
		return self

	def set_bill_email(self, bill_email: str) -> 'OrderCreate':
		"""
		Set BillEmail.

		:param bill_email: str
		:returns: OrderCreate
		"""

		self.bill_email = bill_email
		return self

	def set_bill_phone(self, bill_phone: str) -> 'OrderCreate':
		"""
		Set BillPhone.

		:param bill_phone: str
		:returns: OrderCreate
		"""

		self.bill_phone = bill_phone
		return self

	def set_bill_fax(self, bill_fax: str) -> 'OrderCreate':
		"""
		Set BillFax.

		:param bill_fax: str
		:returns: OrderCreate
		"""

		self.bill_fax = bill_fax
		return self

	def set_bill_company(self, bill_company: str) -> 'OrderCreate':
		"""
		Set BillCompany.

		:param bill_company: str
		:returns: OrderCreate
		"""

		self.bill_company = bill_company
		return self

	def set_bill_address1(self, bill_address1: str) -> 'OrderCreate':
		"""
		Set BillAddress1.

		:param bill_address1: str
		:returns: OrderCreate
		"""

		self.bill_address1 = bill_address1
		return self

	def set_bill_address2(self, bill_address2: str) -> 'OrderCreate':
		"""
		Set BillAddress2.

		:param bill_address2: str
		:returns: OrderCreate
		"""

		self.bill_address2 = bill_address2
		return self

	def set_bill_city(self, bill_city: str) -> 'OrderCreate':
		"""
		Set BillCity.

		:param bill_city: str
		:returns: OrderCreate
		"""

		self.bill_city = bill_city
		return self

	def set_bill_state(self, bill_state: str) -> 'OrderCreate':
		"""
		Set BillState.

		:param bill_state: str
		:returns: OrderCreate
		"""

		self.bill_state = bill_state
		return self

	def set_bill_zip(self, bill_zip: str) -> 'OrderCreate':
		"""
		Set BillZip.

		:param bill_zip: str
		:returns: OrderCreate
		"""

		self.bill_zip = bill_zip
		return self

	def set_bill_country(self, bill_country: str) -> 'OrderCreate':
		"""
		Set BillCountry.

		:param bill_country: str
		:returns: OrderCreate
		"""

		self.bill_country = bill_country
		return self

	def set_items(self, items: list) -> 'OrderCreate':
		"""
		Set Items.

		:param items: {OrderItem[]}
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in items:
			if not isinstance(e, merchantapi.model.OrderItem):
				raise Exception("")
		self.items = items
		return self

	def set_products(self, products: list) -> 'OrderCreate':
		"""
		Set Products.

		:param products: {OrderProduct[]}
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in products:
			if not isinstance(e, merchantapi.model.OrderProduct):
				raise Exception("")
		self.products = products
		return self

	def set_charges(self, charges: list) -> 'OrderCreate':
		"""
		Set Charges.

		:param charges: {OrderCharge[]}
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in charges:
			if not isinstance(e, merchantapi.model.OrderCharge):
				raise Exception("")
		self.charges = charges
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'OrderCreate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: OrderCreate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	def set_shipping_module_code(self, shipping_module_code: str) -> 'OrderCreate':
		"""
		Set Shipping_Module_Code.

		:param shipping_module_code: str
		:returns: OrderCreate
		"""

		self.shipping_module_code = shipping_module_code
		return self

	def set_shipping_module_data(self, shipping_module_data: str) -> 'OrderCreate':
		"""
		Set Shipping_Module_Data.

		:param shipping_module_data: str
		:returns: OrderCreate
		"""

		self.shipping_module_data = shipping_module_data
		return self

	def set_calculate_charges(self, calculate_charges: bool) -> 'OrderCreate':
		"""
		Set CalculateCharges.

		:param calculate_charges: bool
		:returns: OrderCreate
		"""

		self.calculate_charges = calculate_charges
		return self

	def set_trigger_fulfillment_modules(self, trigger_fulfillment_modules: bool) -> 'OrderCreate':
		"""
		Set TriggerFulfillmentModules.

		:param trigger_fulfillment_modules: bool
		:returns: OrderCreate
		"""

		self.trigger_fulfillment_modules = trigger_fulfillment_modules
		return self
	
	def add_item(self, item) -> 'OrderCreate':
		"""
		Add Items.

		:param item: OrderItem 
		:raises Exception:
		:returns: {OrderCreate}
		"""

		if isinstance(item, merchantapi.model.OrderItem):
			self.items.append(item)
		elif isinstance(item, dict):
			self.items.append(merchantapi.model.OrderItem(item))
		else:
			raise Exception('Expected instance of OrderItem or dict')
		return self

	def add_items(self, items: list) -> 'OrderCreate':
		"""
		Add many OrderItem.

		:param items: List of OrderItem
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in items:
			if not isinstance(e, merchantapi.model.OrderItem):
				raise Exception('')
			self.items.append(e)

		return self
	
	def add_product(self, product) -> 'OrderCreate':
		"""
		Add Products.

		:param product: OrderProduct 
		:raises Exception:
		:returns: {OrderCreate}
		"""

		if isinstance(product, merchantapi.model.OrderProduct):
			self.products.append(product)
		elif isinstance(product, dict):
			self.products.append(merchantapi.model.OrderProduct(product))
		else:
			raise Exception('Expected instance of OrderProduct or dict')
		return self

	def add_products(self, products: list) -> 'OrderCreate':
		"""
		Add many OrderProduct.

		:param products: List of OrderProduct
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in products:
			if not isinstance(e, merchantapi.model.OrderProduct):
				raise Exception('')
			self.products.append(e)

		return self
	
	def add_charge(self, charge) -> 'OrderCreate':
		"""
		Add Charges.

		:param charge: OrderCharge 
		:raises Exception:
		:returns: {OrderCreate}
		"""

		if isinstance(charge, merchantapi.model.OrderCharge):
			self.charges.append(charge)
		elif isinstance(charge, dict):
			self.charges.append(merchantapi.model.OrderCharge(charge))
		else:
			raise Exception('Expected instance of OrderCharge or dict')
		return self

	def add_charges(self, charges: list) -> 'OrderCreate':
		"""
		Add many OrderCharge.

		:param charges: List of OrderCharge
		:raises Exception:
		:returns: OrderCreate
		"""

		for e in charges:
			if not isinstance(e, merchantapi.model.OrderCharge):
				raise Exception('')
			self.charges.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderCreate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderCreate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderCreate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		if self.ship_first_name is not None:
			data['ShipFirstName'] = self.ship_first_name
		if self.ship_last_name is not None:
			data['ShipLastName'] = self.ship_last_name
		if self.ship_email is not None:
			data['ShipEmail'] = self.ship_email
		if self.ship_phone is not None:
			data['ShipPhone'] = self.ship_phone
		if self.ship_fax is not None:
			data['ShipFax'] = self.ship_fax
		if self.ship_company is not None:
			data['ShipCompany'] = self.ship_company
		if self.ship_address1 is not None:
			data['ShipAddress1'] = self.ship_address1
		if self.ship_address2 is not None:
			data['ShipAddress2'] = self.ship_address2
		if self.ship_city is not None:
			data['ShipCity'] = self.ship_city
		if self.ship_state is not None:
			data['ShipState'] = self.ship_state
		if self.ship_zip is not None:
			data['ShipZip'] = self.ship_zip
		if self.ship_country is not None:
			data['ShipCountry'] = self.ship_country
		if self.ship_residential is not None:
			data['ShipResidential'] = self.ship_residential
		if self.bill_first_name is not None:
			data['BillFirstName'] = self.bill_first_name
		if self.bill_last_name is not None:
			data['BillLastName'] = self.bill_last_name
		if self.bill_email is not None:
			data['BillEmail'] = self.bill_email
		if self.bill_phone is not None:
			data['BillPhone'] = self.bill_phone
		if self.bill_fax is not None:
			data['BillFax'] = self.bill_fax
		if self.bill_company is not None:
			data['BillCompany'] = self.bill_company
		if self.bill_address1 is not None:
			data['BillAddress1'] = self.bill_address1
		if self.bill_address2 is not None:
			data['BillAddress2'] = self.bill_address2
		if self.bill_city is not None:
			data['BillCity'] = self.bill_city
		if self.bill_state is not None:
			data['BillState'] = self.bill_state
		if self.bill_zip is not None:
			data['BillZip'] = self.bill_zip
		if self.bill_country is not None:
			data['BillCountry'] = self.bill_country
		if len(self.items):
			data['Items'] = []

			for f in self.items:
				data['Items'].append(f.to_dict())
		if len(self.products):
			data['Products'] = []

			for f in self.products:
				data['Products'].append(f.to_dict())
		if len(self.charges):
			data['Charges'] = []

			for f in self.charges:
				data['Charges'].append(f.to_dict())
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		if self.shipping_module_code is not None:
			data['Shipping_Module_Code'] = self.shipping_module_code
		if self.shipping_module_data is not None:
			data['Shipping_Module_Data'] = self.shipping_module_data
		if self.calculate_charges is not None:
			data['CalculateCharges'] = self.calculate_charges
		if self.trigger_fulfillment_modules is not None:
			data['TriggerFulfillmentModules'] = self.trigger_fulfillment_modules
		return data
