"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyPageRulesSettings_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copypagerulessettings_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyPageRulesSettingsUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, copy_page_rule: merchantapi.model.CopyPageRule = None):
		"""
		CopyPageRulesSettingsUpdateAssigned Constructor.

		:param client: Client
		:param copy_page_rule: CopyPageRule
		"""

		super().__init__(client)
		self.copy_page_rules_id = None
		self.copy_page_rules_name = None
		self.item_code = None
		self.assigned = None
		if isinstance(copy_page_rule, merchantapi.model.CopyPageRule):
			if copy_page_rule.get_id():
				self.set_copy_page_rules_id(copy_page_rule.get_id())
			elif copy_page_rule.get_name():
				self.set_copy_page_rules_name(copy_page_rule.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyPageRulesSettings_Update_Assigned'

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

	def get_item_code(self) -> str:
		"""
		Get Item_Code.

		:returns: str
		"""

		return self.item_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_copy_page_rules_id(self, copy_page_rules_id: int) -> 'CopyPageRulesSettingsUpdateAssigned':
		"""
		Set CopyPageRules_ID.

		:param copy_page_rules_id: int
		:returns: CopyPageRulesSettingsUpdateAssigned
		"""

		self.copy_page_rules_id = copy_page_rules_id
		return self

	def set_copy_page_rules_name(self, copy_page_rules_name: str) -> 'CopyPageRulesSettingsUpdateAssigned':
		"""
		Set CopyPageRules_Name.

		:param copy_page_rules_name: str
		:returns: CopyPageRulesSettingsUpdateAssigned
		"""

		self.copy_page_rules_name = copy_page_rules_name
		return self

	def set_item_code(self, item_code: str) -> 'CopyPageRulesSettingsUpdateAssigned':
		"""
		Set Item_Code.

		:param item_code: str
		:returns: CopyPageRulesSettingsUpdateAssigned
		"""

		self.item_code = item_code
		return self

	def set_assigned(self, assigned: bool) -> 'CopyPageRulesSettingsUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CopyPageRulesSettingsUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyPageRulesSettingsUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyPageRulesSettingsUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyPageRulesSettingsUpdateAssigned(self, http_response, data)

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

		data['Item_Code'] = self.item_code
		data['Assigned'] = self.assigned
		return data
