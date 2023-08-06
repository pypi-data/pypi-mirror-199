"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request BranchCSSResourceVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branchcssresourceversionlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BranchCSSResourceVersionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_sort_fields = [
		'id',
		'res_id',
		'code',
		'type',
		'is_global',
		'active',
		'file',
		'templ_id',
		'user_id',
		'user_name',
		'source_user_id',
		'source_user_name'
	]

	available_on_demand_columns = [
		'source',
		'linkedpages',
		'linkedresources',
		'source_notes'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchCSSResourceVersionListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.changeset_id = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'BranchCSSResourceVersionList_Load_Query'

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

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_branch_id(self, branch_id: int) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchCSSResourceVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchCSSResourceVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchCSSResourceVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchCSSResourceVersionListLoadQuery(self, http_response, data)

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
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		return data
