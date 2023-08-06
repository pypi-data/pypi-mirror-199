"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PageList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pagelist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'code',
		'name',
		'secure',
		'title',
		'cache',
		'admin',
		'layout'
	]

	available_sort_fields = [
		'code',
		'name',
		'secure',
		'title',
		'cache',
		'admin',
		'layout'
	]

	available_on_demand_columns = [
		'notes',
		'source',
		'settings',
		'url',
		'uris'
	]

	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		PageListLoadQuery Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())
			elif branch.get_name():
				self.set_edit_branch(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PageList_Load_Query'

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

	def set_branch_id(self, branch_id: int) -> 'PageListLoadQuery':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: PageListLoadQuery
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'PageListLoadQuery':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: PageListLoadQuery
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'PageListLoadQuery':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: PageListLoadQuery
		"""

		self.edit_branch = edit_branch
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageListLoadQuery(self, http_response, data)

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

		return data
