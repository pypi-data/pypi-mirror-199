"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ChangesetList_Merge. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetlist_merge
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ChangesetListMerge(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		ChangesetListMerge Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.source_changeset_ids = []
		self.destination_branch_id = None
		self.notes = None
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_destination_branch_id(branch.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetList_Merge'

	def get_source_changeset_ids(self):
		"""
		Get Source_Changeset_IDs.

		:returns: list
		"""

		return self.source_changeset_ids

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

	def set_destination_branch_id(self, destination_branch_id: int) -> 'ChangesetListMerge':
		"""
		Set Destination_Branch_ID.

		:param destination_branch_id: int
		:returns: ChangesetListMerge
		"""

		self.destination_branch_id = destination_branch_id
		return self

	def set_notes(self, notes: str) -> 'ChangesetListMerge':
		"""
		Set Notes.

		:param notes: str
		:returns: ChangesetListMerge
		"""

		self.notes = notes
		return self
	
	def add_source_changeset_id(self, source_changeset_id) -> 'ChangesetListMerge':
		"""
		Add Source_Changeset_IDs.

		:param source_changeset_id: int
		:returns: {ChangesetListMerge}
		"""

		self.source_changeset_ids.append(source_changeset_id)
		return self

	def add_changeset(self, changeset: merchantapi.model.Changeset) -> 'ChangesetListMerge':
		"""
		Add Changeset model.

		:param changeset: Changeset
		:raises Exception:
		:returns: ChangesetListMerge
		"""
		if not isinstance(changeset, merchantapi.model.Changeset):
			raise Exception('Expected an instance of Changeset')

		if changeset.get_id():
			self.source_changeset_ids.append(changeset.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetListMerge':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetListMerge':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetListMerge(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.destination_branch_id is not None:
			data['Destination_Branch_ID'] = self.destination_branch_id

		data['Source_Changeset_IDs'] = self.source_changeset_ids
		if self.notes is not None:
			data['Notes'] = self.notes
		return data
