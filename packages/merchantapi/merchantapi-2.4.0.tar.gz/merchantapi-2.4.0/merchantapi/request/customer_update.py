"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Customer_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customer_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerUpdate Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.customer_password_email = None
		self.customer_password = None
		self.customer_ship_residential = None
		self.customer_ship_first_name = None
		self.customer_ship_last_name = None
		self.customer_ship_email = None
		self.customer_ship_company = None
		self.customer_ship_phone = None
		self.customer_ship_fax = None
		self.customer_ship_address1 = None
		self.customer_ship_address2 = None
		self.customer_ship_city = None
		self.customer_ship_state = None
		self.customer_ship_zip = None
		self.customer_ship_country = None
		self.customer_bill_first_name = None
		self.customer_bill_last_name = None
		self.customer_bill_email = None
		self.customer_bill_company = None
		self.customer_bill_phone = None
		self.customer_bill_fax = None
		self.customer_bill_address1 = None
		self.customer_bill_address2 = None
		self.customer_bill_city = None
		self.customer_bill_state = None
		self.customer_bill_zip = None
		self.customer_bill_country = None
		self.customer_tax_exempt = None
		self.customer_business_account = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

			self.set_customer_login(customer.get_login())
			self.set_customer_password_email(customer.get_password_email())
			self.set_customer_ship_residential(customer.get_shipping_residential())
			self.set_customer_ship_first_name(customer.get_ship_first_name())
			self.set_customer_ship_last_name(customer.get_ship_last_name())
			self.set_customer_ship_email(customer.get_ship_email())
			self.set_customer_ship_company(customer.get_ship_company())
			self.set_customer_ship_phone(customer.get_ship_phone())
			self.set_customer_ship_fax(customer.get_ship_fax())
			self.set_customer_ship_address1(customer.get_ship_address1())
			self.set_customer_ship_address2(customer.get_ship_address2())
			self.set_customer_ship_city(customer.get_ship_city())
			self.set_customer_ship_state(customer.get_ship_state())
			self.set_customer_ship_zip(customer.get_ship_zip())
			self.set_customer_ship_country(customer.get_ship_country())
			self.set_customer_bill_first_name(customer.get_bill_first_name())
			self.set_customer_bill_last_name(customer.get_bill_last_name())
			self.set_customer_bill_email(customer.get_bill_email())
			self.set_customer_bill_company(customer.get_bill_company())
			self.set_customer_bill_phone(customer.get_bill_phone())
			self.set_customer_bill_fax(customer.get_bill_fax())
			self.set_customer_bill_address1(customer.get_bill_address1())
			self.set_customer_bill_address2(customer.get_bill_address2())
			self.set_customer_bill_city(customer.get_bill_city())
			self.set_customer_bill_state(customer.get_bill_state())
			self.set_customer_bill_zip(customer.get_bill_zip())
			self.set_customer_bill_country(customer.get_bill_country())
			self.set_customer_tax_exempt(customer.get_tax_exempt())
			self.set_customer_business_account(customer.get_business_title())

			if customer.get_custom_field_values():
				self.set_custom_field_values(customer.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Customer_Update'

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

	def get_customer_password_email(self) -> str:
		"""
		Get Customer_PasswordEmail.

		:returns: str
		"""

		return self.customer_password_email

	def get_customer_password(self) -> str:
		"""
		Get Customer_Password.

		:returns: str
		"""

		return self.customer_password

	def get_customer_ship_residential(self) -> bool:
		"""
		Get Customer_ShipResidential.

		:returns: bool
		"""

		return self.customer_ship_residential

	def get_customer_ship_first_name(self) -> str:
		"""
		Get Customer_ShipFirstName.

		:returns: str
		"""

		return self.customer_ship_first_name

	def get_customer_ship_last_name(self) -> str:
		"""
		Get Customer_ShipLastName.

		:returns: str
		"""

		return self.customer_ship_last_name

	def get_customer_ship_email(self) -> str:
		"""
		Get Customer_ShipEmail.

		:returns: str
		"""

		return self.customer_ship_email

	def get_customer_ship_company(self) -> str:
		"""
		Get Customer_ShipCompany.

		:returns: str
		"""

		return self.customer_ship_company

	def get_customer_ship_phone(self) -> str:
		"""
		Get Customer_ShipPhone.

		:returns: str
		"""

		return self.customer_ship_phone

	def get_customer_ship_fax(self) -> str:
		"""
		Get Customer_ShipFax.

		:returns: str
		"""

		return self.customer_ship_fax

	def get_customer_ship_address1(self) -> str:
		"""
		Get Customer_ShipAddress1.

		:returns: str
		"""

		return self.customer_ship_address1

	def get_customer_ship_address2(self) -> str:
		"""
		Get Customer_ShipAddress2.

		:returns: str
		"""

		return self.customer_ship_address2

	def get_customer_ship_city(self) -> str:
		"""
		Get Customer_ShipCity.

		:returns: str
		"""

		return self.customer_ship_city

	def get_customer_ship_state(self) -> str:
		"""
		Get Customer_ShipState.

		:returns: str
		"""

		return self.customer_ship_state

	def get_customer_ship_zip(self) -> str:
		"""
		Get Customer_ShipZip.

		:returns: str
		"""

		return self.customer_ship_zip

	def get_customer_ship_country(self) -> str:
		"""
		Get Customer_ShipCountry.

		:returns: str
		"""

		return self.customer_ship_country

	def get_customer_bill_first_name(self) -> str:
		"""
		Get Customer_BillFirstName.

		:returns: str
		"""

		return self.customer_bill_first_name

	def get_customer_bill_last_name(self) -> str:
		"""
		Get Customer_BillLastName.

		:returns: str
		"""

		return self.customer_bill_last_name

	def get_customer_bill_email(self) -> str:
		"""
		Get Customer_BillEmail.

		:returns: str
		"""

		return self.customer_bill_email

	def get_customer_bill_company(self) -> str:
		"""
		Get Customer_BillCompany.

		:returns: str
		"""

		return self.customer_bill_company

	def get_customer_bill_phone(self) -> str:
		"""
		Get Customer_BillPhone.

		:returns: str
		"""

		return self.customer_bill_phone

	def get_customer_bill_fax(self) -> str:
		"""
		Get Customer_BillFax.

		:returns: str
		"""

		return self.customer_bill_fax

	def get_customer_bill_address1(self) -> str:
		"""
		Get Customer_BillAddress1.

		:returns: str
		"""

		return self.customer_bill_address1

	def get_customer_bill_address2(self) -> str:
		"""
		Get Customer_BillAddress2.

		:returns: str
		"""

		return self.customer_bill_address2

	def get_customer_bill_city(self) -> str:
		"""
		Get Customer_BillCity.

		:returns: str
		"""

		return self.customer_bill_city

	def get_customer_bill_state(self) -> str:
		"""
		Get Customer_BillState.

		:returns: str
		"""

		return self.customer_bill_state

	def get_customer_bill_zip(self) -> str:
		"""
		Get Customer_BillZip.

		:returns: str
		"""

		return self.customer_bill_zip

	def get_customer_bill_country(self) -> str:
		"""
		Get Customer_BillCountry.

		:returns: str
		"""

		return self.customer_bill_country

	def get_customer_tax_exempt(self) -> bool:
		"""
		Get Customer_Tax_Exempt.

		:returns: bool
		"""

		return self.customer_tax_exempt

	def get_customer_business_account(self) -> str:
		"""
		Get Customer_BusinessAccount.

		:returns: str
		"""

		return self.customer_business_account

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_customer_id(self, customer_id: int) -> 'CustomerUpdate':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerUpdate
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerUpdate':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerUpdate
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerUpdate':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerUpdate
		"""

		self.customer_login = customer_login
		return self

	def set_customer_password_email(self, customer_password_email: str) -> 'CustomerUpdate':
		"""
		Set Customer_PasswordEmail.

		:param customer_password_email: str
		:returns: CustomerUpdate
		"""

		self.customer_password_email = customer_password_email
		return self

	def set_customer_password(self, customer_password: str) -> 'CustomerUpdate':
		"""
		Set Customer_Password.

		:param customer_password: str
		:returns: CustomerUpdate
		"""

		self.customer_password = customer_password
		return self

	def set_customer_ship_residential(self, customer_ship_residential: bool) -> 'CustomerUpdate':
		"""
		Set Customer_ShipResidential.

		:param customer_ship_residential: bool
		:returns: CustomerUpdate
		"""

		self.customer_ship_residential = customer_ship_residential
		return self

	def set_customer_ship_first_name(self, customer_ship_first_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipFirstName.

		:param customer_ship_first_name: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_first_name = customer_ship_first_name
		return self

	def set_customer_ship_last_name(self, customer_ship_last_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipLastName.

		:param customer_ship_last_name: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_last_name = customer_ship_last_name
		return self

	def set_customer_ship_email(self, customer_ship_email: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipEmail.

		:param customer_ship_email: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_email = customer_ship_email
		return self

	def set_customer_ship_company(self, customer_ship_company: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipCompany.

		:param customer_ship_company: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_company = customer_ship_company
		return self

	def set_customer_ship_phone(self, customer_ship_phone: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipPhone.

		:param customer_ship_phone: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_phone = customer_ship_phone
		return self

	def set_customer_ship_fax(self, customer_ship_fax: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipFax.

		:param customer_ship_fax: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_fax = customer_ship_fax
		return self

	def set_customer_ship_address1(self, customer_ship_address1: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipAddress1.

		:param customer_ship_address1: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_address1 = customer_ship_address1
		return self

	def set_customer_ship_address2(self, customer_ship_address2: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipAddress2.

		:param customer_ship_address2: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_address2 = customer_ship_address2
		return self

	def set_customer_ship_city(self, customer_ship_city: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipCity.

		:param customer_ship_city: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_city = customer_ship_city
		return self

	def set_customer_ship_state(self, customer_ship_state: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipState.

		:param customer_ship_state: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_state = customer_ship_state
		return self

	def set_customer_ship_zip(self, customer_ship_zip: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipZip.

		:param customer_ship_zip: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_zip = customer_ship_zip
		return self

	def set_customer_ship_country(self, customer_ship_country: str) -> 'CustomerUpdate':
		"""
		Set Customer_ShipCountry.

		:param customer_ship_country: str
		:returns: CustomerUpdate
		"""

		self.customer_ship_country = customer_ship_country
		return self

	def set_customer_bill_first_name(self, customer_bill_first_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillFirstName.

		:param customer_bill_first_name: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_first_name = customer_bill_first_name
		return self

	def set_customer_bill_last_name(self, customer_bill_last_name: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillLastName.

		:param customer_bill_last_name: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_last_name = customer_bill_last_name
		return self

	def set_customer_bill_email(self, customer_bill_email: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillEmail.

		:param customer_bill_email: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_email = customer_bill_email
		return self

	def set_customer_bill_company(self, customer_bill_company: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillCompany.

		:param customer_bill_company: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_company = customer_bill_company
		return self

	def set_customer_bill_phone(self, customer_bill_phone: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillPhone.

		:param customer_bill_phone: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_phone = customer_bill_phone
		return self

	def set_customer_bill_fax(self, customer_bill_fax: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillFax.

		:param customer_bill_fax: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_fax = customer_bill_fax
		return self

	def set_customer_bill_address1(self, customer_bill_address1: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillAddress1.

		:param customer_bill_address1: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_address1 = customer_bill_address1
		return self

	def set_customer_bill_address2(self, customer_bill_address2: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillAddress2.

		:param customer_bill_address2: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_address2 = customer_bill_address2
		return self

	def set_customer_bill_city(self, customer_bill_city: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillCity.

		:param customer_bill_city: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_city = customer_bill_city
		return self

	def set_customer_bill_state(self, customer_bill_state: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillState.

		:param customer_bill_state: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_state = customer_bill_state
		return self

	def set_customer_bill_zip(self, customer_bill_zip: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillZip.

		:param customer_bill_zip: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_zip = customer_bill_zip
		return self

	def set_customer_bill_country(self, customer_bill_country: str) -> 'CustomerUpdate':
		"""
		Set Customer_BillCountry.

		:param customer_bill_country: str
		:returns: CustomerUpdate
		"""

		self.customer_bill_country = customer_bill_country
		return self

	def set_customer_tax_exempt(self, customer_tax_exempt: bool) -> 'CustomerUpdate':
		"""
		Set Customer_Tax_Exempt.

		:param customer_tax_exempt: bool
		:returns: CustomerUpdate
		"""

		self.customer_tax_exempt = customer_tax_exempt
		return self

	def set_customer_business_account(self, customer_business_account: str) -> 'CustomerUpdate':
		"""
		Set Customer_BusinessAccount.

		:param customer_business_account: str
		:returns: CustomerUpdate
		"""

		self.customer_business_account = customer_business_account
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'CustomerUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: CustomerUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		elif self.edit_customer is not None:
			data['Edit_Customer'] = self.edit_customer

		if self.customer_login is not None:
			data['Customer_Login'] = self.customer_login
		if self.customer_password_email is not None:
			data['Customer_PasswordEmail'] = self.customer_password_email
		if self.customer_password is not None:
			data['Customer_Password'] = self.customer_password
		if self.customer_ship_residential is not None:
			data['Customer_ShipResidential'] = self.customer_ship_residential
		if self.customer_ship_first_name is not None:
			data['Customer_ShipFirstName'] = self.customer_ship_first_name
		if self.customer_ship_last_name is not None:
			data['Customer_ShipLastName'] = self.customer_ship_last_name
		if self.customer_ship_email is not None:
			data['Customer_ShipEmail'] = self.customer_ship_email
		if self.customer_ship_company is not None:
			data['Customer_ShipCompany'] = self.customer_ship_company
		if self.customer_ship_phone is not None:
			data['Customer_ShipPhone'] = self.customer_ship_phone
		if self.customer_ship_fax is not None:
			data['Customer_ShipFax'] = self.customer_ship_fax
		if self.customer_ship_address1 is not None:
			data['Customer_ShipAddress1'] = self.customer_ship_address1
		if self.customer_ship_address2 is not None:
			data['Customer_ShipAddress2'] = self.customer_ship_address2
		if self.customer_ship_city is not None:
			data['Customer_ShipCity'] = self.customer_ship_city
		if self.customer_ship_state is not None:
			data['Customer_ShipState'] = self.customer_ship_state
		if self.customer_ship_zip is not None:
			data['Customer_ShipZip'] = self.customer_ship_zip
		if self.customer_ship_country is not None:
			data['Customer_ShipCountry'] = self.customer_ship_country
		if self.customer_bill_first_name is not None:
			data['Customer_BillFirstName'] = self.customer_bill_first_name
		if self.customer_bill_last_name is not None:
			data['Customer_BillLastName'] = self.customer_bill_last_name
		if self.customer_bill_email is not None:
			data['Customer_BillEmail'] = self.customer_bill_email
		if self.customer_bill_company is not None:
			data['Customer_BillCompany'] = self.customer_bill_company
		if self.customer_bill_phone is not None:
			data['Customer_BillPhone'] = self.customer_bill_phone
		if self.customer_bill_fax is not None:
			data['Customer_BillFax'] = self.customer_bill_fax
		if self.customer_bill_address1 is not None:
			data['Customer_BillAddress1'] = self.customer_bill_address1
		if self.customer_bill_address2 is not None:
			data['Customer_BillAddress2'] = self.customer_bill_address2
		if self.customer_bill_city is not None:
			data['Customer_BillCity'] = self.customer_bill_city
		if self.customer_bill_state is not None:
			data['Customer_BillState'] = self.customer_bill_state
		if self.customer_bill_zip is not None:
			data['Customer_BillZip'] = self.customer_bill_zip
		if self.customer_bill_country is not None:
			data['Customer_BillCountry'] = self.customer_bill_country
		if self.customer_tax_exempt is not None:
			data['Customer_Tax_Exempt'] = self.customer_tax_exempt
		if self.customer_business_account is not None:
			data['Customer_BusinessAccount'] = self.customer_business_account
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
