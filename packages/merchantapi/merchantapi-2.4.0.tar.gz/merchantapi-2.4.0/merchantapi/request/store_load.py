"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Store_Load. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/store_load
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class StoreLoad(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		StoreLoad Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Store_Load'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.StoreLoad':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'StoreLoad':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.StoreLoad(self, http_response, data)
