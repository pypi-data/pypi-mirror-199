"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request FeedURIList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/feedurilist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class FeedURIListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'canonical',
		'status',
		'uri'
	]

	available_sort_fields = [
		'uri'
	]

	def __init__(self, client: Client = None):
		"""
		FeedURIListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.feed_id = None
		self.feed_code = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'FeedURIList_Load_Query'

	def get_feed_id(self) -> int:
		"""
		Get Feed_ID.

		:returns: int
		"""

		return self.feed_id

	def get_feed_code(self) -> str:
		"""
		Get Feed_Code.

		:returns: str
		"""

		return self.feed_code

	def set_feed_id(self, feed_id: int) -> 'FeedURIListLoadQuery':
		"""
		Set Feed_ID.

		:param feed_id: int
		:returns: FeedURIListLoadQuery
		"""

		self.feed_id = feed_id
		return self

	def set_feed_code(self, feed_code: str) -> 'FeedURIListLoadQuery':
		"""
		Set Feed_Code.

		:param feed_code: str
		:returns: FeedURIListLoadQuery
		"""

		self.feed_code = feed_code
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.FeedURIListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'FeedURIListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.FeedURIListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.feed_id is not None:
			data['Feed_ID'] = self.feed_id
		elif self.feed_code is not None:
			data['Feed_Code'] = self.feed_code

		return data
