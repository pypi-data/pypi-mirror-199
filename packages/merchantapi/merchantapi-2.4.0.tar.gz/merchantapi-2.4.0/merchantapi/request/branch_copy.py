"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Branch_Copy. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_copy
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BranchCopy(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchCopy Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.source_branch_id = None
		self.destination_branch_id = None
		self.notes = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_source_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Copy'

	def get_source_branch_id(self) -> int:
		"""
		Get Source_Branch_ID.

		:returns: int
		"""

		return self.source_branch_id

	def get_destination_branch_id(self) -> int:
		"""
		Get Destination_Branch_ID.

		:returns: int
		"""

		return self.destination_branch_id

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: str
		"""

		return self.notes

	def set_source_branch_id(self, source_branch_id: int) -> 'BranchCopy':
		"""
		Set Source_Branch_ID.

		:param source_branch_id: int
		:returns: BranchCopy
		"""

		self.source_branch_id = source_branch_id
		return self

	def set_destination_branch_id(self, destination_branch_id: int) -> 'BranchCopy':
		"""
		Set Destination_Branch_ID.

		:param destination_branch_id: int
		:returns: BranchCopy
		"""

		self.destination_branch_id = destination_branch_id
		return self

	def set_notes(self, notes: str) -> 'BranchCopy':
		"""
		Set Notes.

		:param notes: str
		:returns: BranchCopy
		"""

		self.notes = notes
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchCopy':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchCopy':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchCopy(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.source_branch_id is not None:
			data['Source_Branch_ID'] = self.source_branch_id

		if self.destination_branch_id is not None:
			data['Destination_Branch_ID'] = self.destination_branch_id

		if self.notes is not None:
			data['Notes'] = self.notes
		return data
