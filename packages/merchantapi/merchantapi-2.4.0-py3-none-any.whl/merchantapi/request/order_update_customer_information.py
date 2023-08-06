"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Order_Update_Customer_Information. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/order_update_customer_information
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderUpdateCustomerInformation(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order: merchantapi.model.Order = None):
		"""
		OrderUpdateCustomerInformation Constructor.

		:param client: Client
		:param order: Order
		"""

		super().__init__(client)
		self.order_id = None
		self.customer_id = None
		self.ship_residential = None
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
		if isinstance(order, merchantapi.model.Order):
			self.set_order_id(order.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Order_Update_Customer_Information'

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

	def get_ship_residential(self) -> bool:
		"""
		Get Ship_Residential.

		:returns: bool
		"""

		return self.ship_residential

	def get_ship_first_name(self) -> str:
		"""
		Get Ship_FirstName.

		:returns: str
		"""

		return self.ship_first_name

	def get_ship_last_name(self) -> str:
		"""
		Get Ship_LastName.

		:returns: str
		"""

		return self.ship_last_name

	def get_ship_email(self) -> str:
		"""
		Get Ship_Email.

		:returns: str
		"""

		return self.ship_email

	def get_ship_phone(self) -> str:
		"""
		Get Ship_Phone.

		:returns: str
		"""

		return self.ship_phone

	def get_ship_fax(self) -> str:
		"""
		Get Ship_Fax.

		:returns: str
		"""

		return self.ship_fax

	def get_ship_company(self) -> str:
		"""
		Get Ship_Company.

		:returns: str
		"""

		return self.ship_company

	def get_ship_address1(self) -> str:
		"""
		Get Ship_Address1.

		:returns: str
		"""

		return self.ship_address1

	def get_ship_address2(self) -> str:
		"""
		Get Ship_Address2.

		:returns: str
		"""

		return self.ship_address2

	def get_ship_city(self) -> str:
		"""
		Get Ship_City.

		:returns: str
		"""

		return self.ship_city

	def get_ship_state(self) -> str:
		"""
		Get Ship_State.

		:returns: str
		"""

		return self.ship_state

	def get_ship_zip(self) -> str:
		"""
		Get Ship_Zip.

		:returns: str
		"""

		return self.ship_zip

	def get_ship_country(self) -> str:
		"""
		Get Ship_Country.

		:returns: str
		"""

		return self.ship_country

	def get_bill_first_name(self) -> str:
		"""
		Get Bill_FirstName.

		:returns: str
		"""

		return self.bill_first_name

	def get_bill_last_name(self) -> str:
		"""
		Get Bill_LastName.

		:returns: str
		"""

		return self.bill_last_name

	def get_bill_email(self) -> str:
		"""
		Get Bill_Email.

		:returns: str
		"""

		return self.bill_email

	def get_bill_phone(self) -> str:
		"""
		Get Bill_Phone.

		:returns: str
		"""

		return self.bill_phone

	def get_bill_fax(self) -> str:
		"""
		Get Bill_Fax.

		:returns: str
		"""

		return self.bill_fax

	def get_bill_company(self) -> str:
		"""
		Get Bill_Company.

		:returns: str
		"""

		return self.bill_company

	def get_bill_address1(self) -> str:
		"""
		Get Bill_Address1.

		:returns: str
		"""

		return self.bill_address1

	def get_bill_address2(self) -> str:
		"""
		Get Bill_Address2.

		:returns: str
		"""

		return self.bill_address2

	def get_bill_city(self) -> str:
		"""
		Get Bill_City.

		:returns: str
		"""

		return self.bill_city

	def get_bill_state(self) -> str:
		"""
		Get Bill_State.

		:returns: str
		"""

		return self.bill_state

	def get_bill_zip(self) -> str:
		"""
		Get Bill_Zip.

		:returns: str
		"""

		return self.bill_zip

	def get_bill_country(self) -> str:
		"""
		Get Bill_Country.

		:returns: str
		"""

		return self.bill_country

	def set_order_id(self, order_id: int) -> 'OrderUpdateCustomerInformation':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: OrderUpdateCustomerInformation
		"""

		self.order_id = order_id
		return self

	def set_customer_id(self, customer_id: int) -> 'OrderUpdateCustomerInformation':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: OrderUpdateCustomerInformation
		"""

		self.customer_id = customer_id
		return self

	def set_ship_residential(self, ship_residential: bool) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Residential.

		:param ship_residential: bool
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_residential = ship_residential
		return self

	def set_ship_first_name(self, ship_first_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_FirstName.

		:param ship_first_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_first_name = ship_first_name
		return self

	def set_ship_last_name(self, ship_last_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_LastName.

		:param ship_last_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_last_name = ship_last_name
		return self

	def set_ship_email(self, ship_email: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Email.

		:param ship_email: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_email = ship_email
		return self

	def set_ship_phone(self, ship_phone: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Phone.

		:param ship_phone: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_phone = ship_phone
		return self

	def set_ship_fax(self, ship_fax: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Fax.

		:param ship_fax: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_fax = ship_fax
		return self

	def set_ship_company(self, ship_company: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Company.

		:param ship_company: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_company = ship_company
		return self

	def set_ship_address1(self, ship_address1: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Address1.

		:param ship_address1: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_address1 = ship_address1
		return self

	def set_ship_address2(self, ship_address2: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Address2.

		:param ship_address2: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_address2 = ship_address2
		return self

	def set_ship_city(self, ship_city: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_City.

		:param ship_city: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_city = ship_city
		return self

	def set_ship_state(self, ship_state: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_State.

		:param ship_state: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_state = ship_state
		return self

	def set_ship_zip(self, ship_zip: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Zip.

		:param ship_zip: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_zip = ship_zip
		return self

	def set_ship_country(self, ship_country: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Ship_Country.

		:param ship_country: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.ship_country = ship_country
		return self

	def set_bill_first_name(self, bill_first_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_FirstName.

		:param bill_first_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_first_name = bill_first_name
		return self

	def set_bill_last_name(self, bill_last_name: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_LastName.

		:param bill_last_name: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_last_name = bill_last_name
		return self

	def set_bill_email(self, bill_email: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Email.

		:param bill_email: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_email = bill_email
		return self

	def set_bill_phone(self, bill_phone: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Phone.

		:param bill_phone: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_phone = bill_phone
		return self

	def set_bill_fax(self, bill_fax: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Fax.

		:param bill_fax: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_fax = bill_fax
		return self

	def set_bill_company(self, bill_company: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Company.

		:param bill_company: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_company = bill_company
		return self

	def set_bill_address1(self, bill_address1: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Address1.

		:param bill_address1: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_address1 = bill_address1
		return self

	def set_bill_address2(self, bill_address2: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Address2.

		:param bill_address2: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_address2 = bill_address2
		return self

	def set_bill_city(self, bill_city: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_City.

		:param bill_city: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_city = bill_city
		return self

	def set_bill_state(self, bill_state: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_State.

		:param bill_state: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_state = bill_state
		return self

	def set_bill_zip(self, bill_zip: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Zip.

		:param bill_zip: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_zip = bill_zip
		return self

	def set_bill_country(self, bill_country: str) -> 'OrderUpdateCustomerInformation':
		"""
		Set Bill_Country.

		:param bill_country: str
		:returns: OrderUpdateCustomerInformation
		"""

		self.bill_country = bill_country
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderUpdateCustomerInformation':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderUpdateCustomerInformation':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderUpdateCustomerInformation(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Order_ID'] = self.order_id
		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		if self.ship_residential is not None:
			data['Ship_Residential'] = self.ship_residential
		if self.ship_first_name is not None:
			data['Ship_FirstName'] = self.ship_first_name
		if self.ship_last_name is not None:
			data['Ship_LastName'] = self.ship_last_name
		if self.ship_email is not None:
			data['Ship_Email'] = self.ship_email
		if self.ship_phone is not None:
			data['Ship_Phone'] = self.ship_phone
		if self.ship_fax is not None:
			data['Ship_Fax'] = self.ship_fax
		if self.ship_company is not None:
			data['Ship_Company'] = self.ship_company
		if self.ship_address1 is not None:
			data['Ship_Address1'] = self.ship_address1
		if self.ship_address2 is not None:
			data['Ship_Address2'] = self.ship_address2
		if self.ship_city is not None:
			data['Ship_City'] = self.ship_city
		if self.ship_state is not None:
			data['Ship_State'] = self.ship_state
		if self.ship_zip is not None:
			data['Ship_Zip'] = self.ship_zip
		if self.ship_country is not None:
			data['Ship_Country'] = self.ship_country
		if self.bill_first_name is not None:
			data['Bill_FirstName'] = self.bill_first_name
		if self.bill_last_name is not None:
			data['Bill_LastName'] = self.bill_last_name
		if self.bill_email is not None:
			data['Bill_Email'] = self.bill_email
		if self.bill_phone is not None:
			data['Bill_Phone'] = self.bill_phone
		if self.bill_fax is not None:
			data['Bill_Fax'] = self.bill_fax
		if self.bill_company is not None:
			data['Bill_Company'] = self.bill_company
		if self.bill_address1 is not None:
			data['Bill_Address1'] = self.bill_address1
		if self.bill_address2 is not None:
			data['Bill_Address2'] = self.bill_address2
		if self.bill_city is not None:
			data['Bill_City'] = self.bill_city
		if self.bill_state is not None:
			data['Bill_State'] = self.bill_state
		if self.bill_zip is not None:
			data['Bill_Zip'] = self.bill_zip
		if self.bill_country is not None:
			data['Bill_Country'] = self.bill_country
		return data
