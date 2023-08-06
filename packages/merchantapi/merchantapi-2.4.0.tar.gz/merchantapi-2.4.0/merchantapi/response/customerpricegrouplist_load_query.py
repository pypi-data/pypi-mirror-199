"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for CustomerPriceGroupList_Load_Query.

:see: https://docs.miva.com/json-api/functions/customerpricegrouplist_load_query
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model
from merchantapi.listquery import ListQueryRequest, ListQueryResponse

class CustomerPriceGroupListLoadQuery(ListQueryResponse):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		CustomerPriceGroupListLoadQuery Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.CustomerPriceGroup(e)

	def get_customer_price_groups(self):
		"""
		Get customer_price_groups.

		:returns: list of CustomerPriceGroup
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']
