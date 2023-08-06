"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyPageRulesList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copypageruleslist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyPageRulesListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CopyPageRulesListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.copy_page_rules_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyPageRulesList_Delete'

	def get_copy_page_rules_ids(self):
		"""
		Get CopyPageRules_IDs.

		:returns: list
		"""

		return self.copy_page_rules_ids
	
	def add_copy_page_rule_id(self, copy_page_rule_id) -> 'CopyPageRulesListDelete':
		"""
		Add CopyPageRules_IDs.

		:param copy_page_rule_id: int
		:returns: {CopyPageRulesListDelete}
		"""

		self.copy_page_rules_ids.append(copy_page_rule_id)
		return self

	def add_copy_page_rule(self, copy_page_rule: merchantapi.model.CopyPageRule) -> 'CopyPageRulesListDelete':
		"""
		Add CopyPageRule model.

		:param copy_page_rule: CopyPageRule
		:raises Exception:
		:returns: CopyPageRulesListDelete
		"""
		if not isinstance(copy_page_rule, merchantapi.model.CopyPageRule):
			raise Exception('Expected an instance of CopyPageRule')

		if copy_page_rule.get_id():
			self.copy_page_rules_ids.append(copy_page_rule.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyPageRulesListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyPageRulesListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyPageRulesListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['CopyPageRules_IDs'] = self.copy_page_rules_ids
		return data
