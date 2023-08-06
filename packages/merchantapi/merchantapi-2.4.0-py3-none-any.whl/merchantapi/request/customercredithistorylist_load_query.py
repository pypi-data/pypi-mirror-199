"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerCreditHistoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customercredithistorylist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerCreditHistoryListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'user_name',
		'order_id',
		'txref',
		'descrip',
		'amount',
		'dtstamp',
		'id'
	]

	available_sort_fields = [
		'user_name',
		'order_id',
		'txref',
		'descrip',
		'amount',
		'dtstamp',
		'id'
	]

	available_on_demand_columns = [
		'source'
	]

	def __init__(self, client: Client = None, customer: merchantapi.model.Customer = None):
		"""
		CustomerCreditHistoryListLoadQuery Constructor.

		:param client: Client
		:param customer: Customer
		"""

		super().__init__(client)
		self.customer_id = None
		self.edit_customer = None
		self.customer_login = None
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

		return 'CustomerCreditHistoryList_Load_Query'

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

	def set_customer_id(self, customer_id: int) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: CustomerCreditHistoryListLoadQuery
		"""

		self.customer_id = customer_id
		return self

	def set_edit_customer(self, edit_customer: str) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Set Edit_Customer.

		:param edit_customer: str
		:returns: CustomerCreditHistoryListLoadQuery
		"""

		self.edit_customer = edit_customer
		return self

	def set_customer_login(self, customer_login: str) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Set Customer_Login.

		:param customer_login: str
		:returns: CustomerCreditHistoryListLoadQuery
		"""

		self.customer_login = customer_login
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerCreditHistoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerCreditHistoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerCreditHistoryListLoadQuery(self, http_response, data)

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

		return data
