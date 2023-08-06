"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PrintQueueJobList_Load_Query. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/printqueuejoblist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PrintQueueJobListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'queue_id',
		'store_id',
		'user_id',
		'descrip',
		'job_fmt',
		'job_data',
		'dt_created'
	]

	available_sort_fields = [
		'id',
		'queue_id',
		'store_id',
		'user_id',
		'descrip',
		'job_fmt',
		'job_data',
		'dt_created'
	]

	available_on_demand_columns = [
		'job_data'
	]

	def __init__(self, client: Client = None, print_queue: merchantapi.model.PrintQueue = None):
		"""
		PrintQueueJobListLoadQuery Constructor.

		:param client: Client
		:param print_queue: PrintQueue
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.print_queue_id = None
		self.edit_print_queue = None
		self.print_queue_description = None
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

		return 'PrintQueueJobList_Load_Query'

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

	def set_print_queue_id(self, print_queue_id: int) -> 'PrintQueueJobListLoadQuery':
		"""
		Set PrintQueue_ID.

		:param print_queue_id: int
		:returns: PrintQueueJobListLoadQuery
		"""

		self.print_queue_id = print_queue_id
		return self

	def set_edit_print_queue(self, edit_print_queue: str) -> 'PrintQueueJobListLoadQuery':
		"""
		Set Edit_PrintQueue.

		:param edit_print_queue: str
		:returns: PrintQueueJobListLoadQuery
		"""

		self.edit_print_queue = edit_print_queue
		return self

	def set_print_queue_description(self, print_queue_description: str) -> 'PrintQueueJobListLoadQuery':
		"""
		Set PrintQueue_Description.

		:param print_queue_description: str
		:returns: PrintQueueJobListLoadQuery
		"""

		self.print_queue_description = print_queue_description
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PrintQueueJobListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PrintQueueJobListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PrintQueueJobListLoadQuery(self, http_response, data)

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

		return data
