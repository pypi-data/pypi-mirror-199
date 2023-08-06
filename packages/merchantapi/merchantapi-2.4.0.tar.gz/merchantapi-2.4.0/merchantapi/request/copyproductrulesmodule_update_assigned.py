"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyProductRulesModule_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copyproductrulesmodule_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyProductRulesModuleUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, copy_product_rule: merchantapi.model.CopyProductRule = None):
		"""
		CopyProductRulesModuleUpdateAssigned Constructor.

		:param client: Client
		:param copy_product_rule: CopyProductRule
		"""

		super().__init__(client)
		self.copy_product_rules_id = None
		self.copy_product_rules_name = None
		self.module_code = None
		self.assigned = None
		if isinstance(copy_product_rule, merchantapi.model.CopyProductRule):
			if copy_product_rule.get_id():
				self.set_copy_product_rules_id(copy_product_rule.get_id())
			elif copy_product_rule.get_name():
				self.set_copy_product_rules_name(copy_product_rule.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyProductRulesModule_Update_Assigned'

	def get_copy_product_rules_id(self) -> int:
		"""
		Get CopyProductRules_ID.

		:returns: int
		"""

		return self.copy_product_rules_id

	def get_copy_product_rules_name(self) -> str:
		"""
		Get CopyProductRules_Name.

		:returns: str
		"""

		return self.copy_product_rules_name

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: str
		"""

		return self.module_code

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_copy_product_rules_id(self, copy_product_rules_id: int) -> 'CopyProductRulesModuleUpdateAssigned':
		"""
		Set CopyProductRules_ID.

		:param copy_product_rules_id: int
		:returns: CopyProductRulesModuleUpdateAssigned
		"""

		self.copy_product_rules_id = copy_product_rules_id
		return self

	def set_copy_product_rules_name(self, copy_product_rules_name: str) -> 'CopyProductRulesModuleUpdateAssigned':
		"""
		Set CopyProductRules_Name.

		:param copy_product_rules_name: str
		:returns: CopyProductRulesModuleUpdateAssigned
		"""

		self.copy_product_rules_name = copy_product_rules_name
		return self

	def set_module_code(self, module_code: str) -> 'CopyProductRulesModuleUpdateAssigned':
		"""
		Set Module_Code.

		:param module_code: str
		:returns: CopyProductRulesModuleUpdateAssigned
		"""

		self.module_code = module_code
		return self

	def set_assigned(self, assigned: bool) -> 'CopyProductRulesModuleUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CopyProductRulesModuleUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyProductRulesModuleUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyProductRulesModuleUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyProductRulesModuleUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.copy_product_rules_id is not None:
			data['CopyProductRules_ID'] = self.copy_product_rules_id
		elif self.copy_product_rules_name is not None:
			data['CopyProductRules_Name'] = self.copy_product_rules_name

		data['Module_Code'] = self.module_code
		data['Assigned'] = self.assigned
		return data
