"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Branch_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BranchDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchDelete Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Delete'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def set_branch_id(self, branch_id: int) -> 'BranchDelete':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchDelete
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchDelete':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchDelete
		"""

		self.branch_name = branch_name
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		return data
