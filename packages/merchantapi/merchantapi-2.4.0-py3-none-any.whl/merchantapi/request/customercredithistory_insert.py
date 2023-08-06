"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerCreditHistory_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customercredithistory_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerCreditHistoryInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerCreditHistoryInsert Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
		self.amount = None
		self.description = None
		self.transaction_reference = None
		if isinstance(customer, merchantapi.model.Customer):
			if customer.get_id():
				self.set_customer_id(customer.get_id())
			elif customer.get_login():
				self.set_edit_customer(customer.get_login())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerCreditHistory_Insert'

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

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def get_description(self) -> str:
		"""
		Get Description.

		:returns: str
		"""

		return self.description

	def get_transaction_reference(self) -> str:
		"""
		Get TransactionReference.

		:returns: str
		"""

		return self.transaction_reference

	def set_customer_id(self, customer_id: int) -> 'CustomerCreditHistoryInsert':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerCreditHistoryInsert
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.customer_login = customer_login
		return self

	def set_amount(self, amount: float) -> 'CustomerCreditHistoryInsert':
		"""
		Set Amount.

		:param amount: float
		:returns: CustomerCreditHistoryInsert
		"""

		self.amount = amount
		return self

	def set_description(self, description: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set Description.

		:param description: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.description = description
		return self

	def set_transaction_reference(self, transaction_reference: str) -> 'CustomerCreditHistoryInsert':
		"""
		Set TransactionReference.

		:param transaction_reference: str
		:returns: CustomerCreditHistoryInsert
		"""

		self.transaction_reference = transaction_reference
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerCreditHistoryInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerCreditHistoryInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerCreditHistoryInsert(self, http_response, data)

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
		elif self.customer_login is not None:
			data['Customer_Login'] = self.customer_login

		data['Amount'] = self.amount
		data['Description'] = self.description
		if self.transaction_reference is not None:
			data['TransactionReference'] = self.transaction_reference
		return data
