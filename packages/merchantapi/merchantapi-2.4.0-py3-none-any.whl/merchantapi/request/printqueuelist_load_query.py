"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PrintQueueList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/printqueuelist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PrintQueueListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'descrip'
	]

	available_sort_fields = [
		'descrip'
	]

	def __init__(self, client: Client = None):
		"""
		PrintQueueListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueListLoadQuery(self, http_response, data)
