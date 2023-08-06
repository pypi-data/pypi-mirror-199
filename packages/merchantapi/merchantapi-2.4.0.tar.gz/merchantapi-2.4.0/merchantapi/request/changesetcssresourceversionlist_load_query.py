"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ChangesetCSSResourceVersionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changesetcssresourceversionlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ChangesetCSSResourceVersionListLoadQuery(ListQueryRequest):

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
		'source_notes'
	]

	def __init__(self, client: Client = None, changeset: merchantapi.model.Changeset = None):
		"""
		ChangesetCSSResourceVersionListLoadQuery Constructor.

		:param client: Client
		:param changeset: Changeset
		"""

		super().__init__(client)
		self.changeset_id = None
		if isinstance(changeset, merchantapi.model.Changeset):
			self.set_changeset_id(changeset.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ChangesetCSSResourceVersionList_Load_Query'

	def get_changeset_id(self) -> int:
		"""
		Get Changeset_ID.

		:returns: int
		"""

		return self.changeset_id

	def set_changeset_id(self, changeset_id: int) -> 'ChangesetCSSResourceVersionListLoadQuery':
		"""
		Set Changeset_ID.

		:param changeset_id: int
		:returns: ChangesetCSSResourceVersionListLoadQuery
		"""

		self.changeset_id = changeset_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetCSSResourceVersionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetCSSResourceVersionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetCSSResourceVersionListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Changeset_ID'] = self.get_changeset_id()

		return data
