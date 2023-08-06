"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BranchList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchlist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BranchListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		BranchListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.branch_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchList_Delete'

	def get_branch_ids(self):
		"""
		Get Branch_IDs.

		:returns: list
		"""

		return self.branch_ids
	
	def add_branch_id(self, branch_id) -> 'BranchListDelete':
		"""
		Add Branch_IDs.

		:param branch_id: int
		:returns: {BranchListDelete}
		"""

		self.branch_ids.append(branch_id)
		return self

	def add_branch(self, branch: merchantapi.model.Branch) -> 'BranchListDelete':
		"""
		Add Branch model.

		:param branch: Branch
		:raises Exception:
		:returns: BranchListDelete
		"""
		if not isinstance(branch, merchantapi.model.Branch):
			raise Exception('Expected an instance of Branch')

		if branch.get_id():
			self.branch_ids.append(branch.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Branch_IDs'] = self.branch_ids
		return data
