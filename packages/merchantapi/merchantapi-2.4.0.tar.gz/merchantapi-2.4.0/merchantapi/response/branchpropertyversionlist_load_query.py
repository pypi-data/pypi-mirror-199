"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for BranchPropertyVersionList_Load_Query.

:see: https://docs.miva.com/json-api/functions/branchpropertyversionlist_load_query
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model
from merchantapi.listquery import ListQueryRequest, ListQueryResponse

class BranchPropertyVersionListLoadQuery(ListQueryResponse):
	def __init__(self, request: ListQueryRequest, http_response: HttpResponse, data: dict):
		"""
		BranchPropertyVersionListLoadQuery Constructor.

		:param request: ListQueryRequest
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and 'data' in self.data['data'] and isinstance(self.data['data']['data'], list):
			for i, e in enumerate(self.data['data']['data'], 0):
				self.data['data']['data'][i] = merchantapi.model.BranchPropertyVersion(e)

	def get_branch_property_versions(self):
		"""
		Get branch_property_versions.

		:returns: list of BranchPropertyVersion
		"""

		if self.data['data'] is None or not isinstance(self.data['data']['data'], list):
			return []

		return self.data['data']['data']
