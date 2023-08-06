"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyProductRulesList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copyproductruleslist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyProductRulesListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CopyProductRulesListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.copy_product_rules_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyProductRulesList_Delete'

	def get_copy_product_rules_ids(self):
		"""
		Get CopyProductRules_IDs.

		:returns: list
		"""

		return self.copy_product_rules_ids
	
	def add_copy_product_rule_id(self, copy_product_rule_id) -> 'CopyProductRulesListDelete':
		"""
		Add CopyProductRules_IDs.

		:param copy_product_rule_id: int
		:returns: {CopyProductRulesListDelete}
		"""

		self.copy_product_rules_ids.append(copy_product_rule_id)
		return self

	def add_copy_product_rule(self, copy_product_rule: merchantapi.model.CopyProductRule) -> 'CopyProductRulesListDelete':
		"""
		Add CopyProductRule model.

		:param copy_product_rule: CopyProductRule
		:raises Exception:
		:returns: CopyProductRulesListDelete
		"""
		if not isinstance(copy_product_rule, merchantapi.model.CopyProductRule):
			raise Exception('Expected an instance of CopyProductRule')

		if copy_product_rule.get_id():
			self.copy_product_rules_ids.append(copy_product_rule.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyProductRulesListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyProductRulesListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyProductRulesListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['CopyProductRules_IDs'] = self.copy_product_rules_ids
		return data
