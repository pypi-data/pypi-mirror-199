"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PrintQueueJob_Status. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/printqueuejob_status
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PrintQueueJobStatus(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, print_queue_job: merchantapi.model.PrintQueueJob = None):
		"""
		PrintQueueJobStatus Constructor.

		:param client: Client
		:param print_queue_job: PrintQueueJob
		"""

		super().__init__(client)
		self.print_queue_job_id = None
		if isinstance(print_queue_job, merchantapi.model.PrintQueueJob):
			if print_queue_job.get_id():
				self.set_print_queue_job_id(print_queue_job.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueJob_Status'

	def get_print_queue_job_id(self) -> int:
		"""
		Get PrintQueueJob_ID.

		:returns: int
		"""

		return self.print_queue_job_id

	def set_print_queue_job_id(self, print_queue_job_id: int) -> 'PrintQueueJobStatus':
		"""
		Set PrintQueueJob_ID.

		:param print_queue_job_id: int
		:returns: PrintQueueJobStatus
		"""

		self.print_queue_job_id = print_queue_job_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobStatus':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobStatus':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobStatus(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.print_queue_job_id is not None:
			data['PrintQueueJob_ID'] = self.print_queue_job_id

		return data
