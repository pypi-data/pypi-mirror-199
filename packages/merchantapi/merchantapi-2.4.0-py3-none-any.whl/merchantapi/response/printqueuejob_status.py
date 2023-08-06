"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for PrintQueueJob_Status.

:see: https://docs.miva.com/json-api/functions/printqueuejob_status
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class PrintQueueJobStatus(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PrintQueueJobStatus Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)

	def get_status(self):
		"""
		Get status.

		:returns: string
		"""

		if 'data' in self.data and 'status' in self.data['data']:
			return self.data['data']['status']
		return None
