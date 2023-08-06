"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Note_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/note_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class NoteInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		NoteInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.note_text = None
		self.customer_id = None
		self.account_id = None
		self.order_id = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Note_Insert'

	def get_note_text(self) -> str:
		"""
		Get NoteText.

		:returns: str
		"""

		return self.note_text

	def get_customer_id(self) -> int:
		"""
		Get Customer_ID.

		:returns: int
		"""

		return self.customer_id

	def get_account_id(self) -> int:
		"""
		Get Account_ID.

		:returns: int
		"""

		return self.account_id

	def get_order_id(self) -> int:
		"""
		Get Order_ID.

		:returns: int
		"""

		return self.order_id

	def set_note_text(self, note_text: str) -> 'NoteInsert':
		"""
		Set NoteText.

		:param note_text: str
		:returns: NoteInsert
		"""

		self.note_text = note_text
		return self

	def set_customer_id(self, customer_id: int) -> 'NoteInsert':
		"""
		Set Customer_ID.

		:param customer_id: int
		:returns: NoteInsert
		"""

		self.customer_id = customer_id
		return self

	def set_account_id(self, account_id: int) -> 'NoteInsert':
		"""
		Set Account_ID.

		:param account_id: int
		:returns: NoteInsert
		"""

		self.account_id = account_id
		return self

	def set_order_id(self, order_id: int) -> 'NoteInsert':
		"""
		Set Order_ID.

		:param order_id: int
		:returns: NoteInsert
		"""

		self.order_id = order_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['NoteText'] = self.note_text
		if self.customer_id is not None:
			data['Customer_ID'] = self.customer_id
		if self.account_id is not None:
			data['Account_ID'] = self.account_id
		if self.order_id is not None:
			data['Order_ID'] = self.order_id
		return data
