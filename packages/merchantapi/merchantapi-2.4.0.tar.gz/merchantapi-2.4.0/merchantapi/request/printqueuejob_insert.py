"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PrintQueueJob_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/printqueuejob_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PrintQueueJobInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, print_queue: merchantapi.model.PrintQueue = None):
		"""
		PrintQueueJobInsert Constructor.

		:param client: Client
		:param print_queue: PrintQueue
		"""

		super().__init__(client)
		self.print_queue_id = None
		self.edit_print_queue = None
		self.print_queue_description = None
		self.print_queue_job_description = None
		self.print_queue_job_format = None
		self.print_queue_job_data = None
		if isinstance(print_queue, merchantapi.model.PrintQueue):
			if print_queue.get_id():
				self.set_print_queue_id(print_queue.get_id())
			elif print_queue.get_description():
				self.set_edit_print_queue(print_queue.get_description())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PrintQueueJob_Insert'

	def get_print_queue_id(self) -> int:
		"""
		Get PrintQueue_ID.

		:returns: int
		"""

		return self.print_queue_id

	def get_edit_print_queue(self) -> str:
		"""
		Get Edit_PrintQueue.

		:returns: str
		"""

		return self.edit_print_queue

	def get_print_queue_description(self) -> str:
		"""
		Get PrintQueue_Description.

		:returns: str
		"""

		return self.print_queue_description

	def get_print_queue_job_description(self) -> str:
		"""
		Get PrintQueueJob_Description.

		:returns: str
		"""

		return self.print_queue_job_description

	def get_print_queue_job_format(self) -> str:
		"""
		Get PrintQueueJob_Format.

		:returns: str
		"""

		return self.print_queue_job_format

	def get_print_queue_job_data(self) -> str:
		"""
		Get PrintQueueJob_Data.

		:returns: str
		"""

		return self.print_queue_job_data

	def set_print_queue_id(self, print_queue_id: int) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueue_ID.

		:param print_queue_id: int
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_id = print_queue_id
		return self

	def set_edit_print_queue(self, edit_print_queue: str) -> 'PrintQueueJobInsert':
		"""
		Set Edit_PrintQueue.

		:param edit_print_queue: str
		:returns: PrintQueueJobInsert
		"""

		self.edit_print_queue = edit_print_queue
		return self

	def set_print_queue_description(self, print_queue_description: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueue_Description.

		:param print_queue_description: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_description = print_queue_description
		return self

	def set_print_queue_job_description(self, print_queue_job_description: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueueJob_Description.

		:param print_queue_job_description: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_job_description = print_queue_job_description
		return self

	def set_print_queue_job_format(self, print_queue_job_format: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueueJob_Format.

		:param print_queue_job_format: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_job_format = print_queue_job_format
		return self

	def set_print_queue_job_data(self, print_queue_job_data: str) -> 'PrintQueueJobInsert':
		"""
		Set PrintQueueJob_Data.

		:param print_queue_job_data: str
		:returns: PrintQueueJobInsert
		"""

		self.print_queue_job_data = print_queue_job_data
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.print_queue_id is not None:
			data['PrintQueue_ID'] = self.print_queue_id
		elif self.edit_print_queue is not None:
			data['Edit_PrintQueue'] = self.edit_print_queue
		elif self.print_queue_description is not None:
			data['PrintQueue_Description'] = self.print_queue_description

		if self.print_queue_job_description is not None:
			data['PrintQueueJob_Description'] = self.print_queue_job_description
		if self.print_queue_job_format is not None:
			data['PrintQueueJob_Format'] = self.print_queue_job_format
		if self.print_queue_job_data is not None:
			data['PrintQueueJob_Data'] = self.print_queue_job_data
		return data
