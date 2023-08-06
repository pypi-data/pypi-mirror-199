"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyPageRulesSettingsList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copypagerulessettingslist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyPageRulesSettingsListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'code',
		'module_name'
	]

	available_sort_fields = [
		'id',
		'code',
		'module_name'
	]

	def __init__(self, client: Client = None):
		"""
		CopyPageRulesSettingsListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.copy_page_rules_id = None
		self.copy_page_rules_name = None
		self.assigned = None
		self.unassigned = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyPageRulesSettingsList_Load_Query'

	def get_copy_page_rules_id(self) -> int:
		"""
		Get CopyPageRules_ID.

		:returns: int
		"""

		return self.copy_page_rules_id

	def get_copy_page_rules_name(self) -> str:
		"""
		Get CopyPageRules_Name.

		:returns: str
		"""

		return self.copy_page_rules_name

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def get_unassigned(self) -> bool:
		"""
		Get Unassigned.

		:returns: bool
		"""

		return self.unassigned

	def set_copy_page_rules_id(self, copy_page_rules_id: int) -> 'CopyPageRulesSettingsListLoadQuery':
		"""
		Set CopyPageRules_ID.

		:param copy_page_rules_id: int
		:returns: CopyPageRulesSettingsListLoadQuery
		"""

		self.copy_page_rules_id = copy_page_rules_id
		return self

	def set_copy_page_rules_name(self, copy_page_rules_name: str) -> 'CopyPageRulesSettingsListLoadQuery':
		"""
		Set CopyPageRules_Name.

		:param copy_page_rules_name: str
		:returns: CopyPageRulesSettingsListLoadQuery
		"""

		self.copy_page_rules_name = copy_page_rules_name
		return self

	def set_assigned(self, assigned: bool) -> 'CopyPageRulesSettingsListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CopyPageRulesSettingsListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CopyPageRulesSettingsListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CopyPageRulesSettingsListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyPageRulesSettingsListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyPageRulesSettingsListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyPageRulesSettingsListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.copy_page_rules_id is not None:
			data['CopyPageRules_ID'] = self.copy_page_rules_id
		elif self.copy_page_rules_name is not None:
			data['CopyPageRules_Name'] = self.copy_page_rules_name

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
