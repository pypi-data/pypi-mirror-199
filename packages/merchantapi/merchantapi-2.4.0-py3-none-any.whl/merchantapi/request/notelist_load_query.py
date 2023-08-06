"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request NoteList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/notelist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class NoteListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'notetext',
		'dtstamp',
		'cust_id',
		'account_id',
		'order_id',
		'admin_user',
		'cust_login',
		'business_title'
	]

	available_sort_fields = [
		'id',
		'notetext',
		'dtstamp',
		'cust_id',
		'account_id',
		'order_id',
		'admin_user',
		'cust_login',
		'business_title'
	]

	def __init__(self, client: Client = None):
		"""
		NoteListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'NoteList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteListLoadQuery(self, http_response, data)
