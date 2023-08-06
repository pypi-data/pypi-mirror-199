"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for PrintQueueJob_Insert.

:see: https://docs.miva.com/json-api/functions/printqueuejob_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class PrintQueueJobInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PrintQueueJobInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.PrintQueueJob(self.data['data'])

	def get_print_queue_job(self) -> merchantapi.model.PrintQueueJob:
		"""
		Get print_queue_job.

		:returns: PrintQueueJob
		"""

		return {} if 'data' not in self.data else self.data['data']
