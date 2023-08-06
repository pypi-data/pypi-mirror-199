"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BranchList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BranchListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'immutable',
		'branchkey',
		'name',
		'framework'
	]

	available_sort_fields = [
		'id',
		'immutable',
		'branchkey',
		'name',
		'framework'
	]

	def __init__(self, client: Client = None):
		"""
		BranchListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchListLoadQuery(self, http_response, data)
