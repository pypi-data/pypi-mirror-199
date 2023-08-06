"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Branch_Create. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/branch_create
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class BranchCreate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		BranchCreate Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.parent_branch_id = None
		self.name = None
		self.color = None
		self.changeset_id = None
		self.tags = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_parent_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Branch_Create'

	def get_parent_branch_id(self) -> int:
		"""
		Get Parent_Branch_ID.

		:returns: int
		"""

		return self.parent_branch_id

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_color(self) -> str:
		"""
		Get Color.

		:returns: str
		"""

		return self.color

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def get_tags(self) -> str:
		"""
		Get Tags.

		:returns: str
		"""

		return self.tags

	def set_parent_branch_id(self, parent_branch_id: int) -> 'BranchCreate':
		"""
		Set Parent_Branch_ID.

		:param parent_branch_id: int
		:returns: BranchCreate
		"""

		self.parent_branch_id = parent_branch_id
		return self

	def set_name(self, name: str) -> 'BranchCreate':
		"""
		Set Name.

		:param name: str
		:returns: BranchCreate
		"""

		self.name = name
		return self

	def set_color(self, color: str) -> 'BranchCreate':
		"""
		Set Color.

		:param color: str
		:returns: BranchCreate
		"""

		self.color = color
		return self

	def set_changeset_id(self, changeset_id: int) -> 'BranchCreate':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: BranchCreate
		"""

		self.changeset_id = changeset_id
		return self

	def set_tags(self, tags: str) -> 'BranchCreate':
		"""
		Set Tags.

		:param tags: str
		:returns: BranchCreate
		"""

		self.tags = tags
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.BranchCreate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'BranchCreate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.BranchCreate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.parent_branch_id is not None:
			data['Parent_Branch_ID'] = self.parent_branch_id

		if self.name is not None:
			data['Name'] = self.name
		if self.color is not None:
			data['Color'] = self.color
		if self.changeset_id is not None:
			data['Changeset_ID'] = self.changeset_id
		if self.tags is not None:
			data['Tags'] = self.tags
		return data
