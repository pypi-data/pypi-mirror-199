"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request URIList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/urilist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class URIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'uri',
		'screen',
		'status',
		'canonical',
		'store_name',
		'page_code',
		'page_name',
		'category_code',
		'category_name',
		'product_code',
		'product_sku',
		'product_name',
		'feed_code',
		'feed_name'
	]

	available_sort_fields = [
		'id',
		'uri',
		'screen',
		'status',
		'canonical',
		'store_name',
		'page_code',
		'page_name',
		'category_code',
		'category_name',
		'product_code',
		'product_sku',
		'product_name',
		'feed_code',
		'feed_name'
	]

	def __init__(self, client: Client = None):
		"""
		URIListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'URIList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.URIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'URIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.URIListLoadQuery(self, http_response, data)
