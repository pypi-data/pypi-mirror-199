"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyProductRulesCustomFieldList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copyproductrulescustomfieldlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyProductRulesCustomFieldListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'module_name',
		'field_code',
		'field_name'
	]

	available_sort_fields = [
		'module_name',
		'field_code',
		'field_name'
	]

	def __init__(self, client: Client = None, copy_product_rule: merchantapi.model.CopyProductRule = None):
		"""
		CopyProductRulesCustomFieldListLoadQuery Constructor.

		:param client: Client
		:param copy_product_rule: CopyProductRule
		"""

		super().__init__(client)
		self.copy_product_rules_id = None
		self.copy_product_rules_name = None
		self.assigned = None
		self.unassigned = None
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

		return 'CopyProductRulesCustomFieldList_Load_Query'

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

	def set_copy_product_rules_id(self, copy_product_rules_id: int) -> 'CopyProductRulesCustomFieldListLoadQuery':
		"""
		Set CopyProductRules_ID.

		:param copy_product_rules_id: int
		:returns: CopyProductRulesCustomFieldListLoadQuery
		"""

		self.copy_product_rules_id = copy_product_rules_id
		return self

	def set_copy_product_rules_name(self, copy_product_rules_name: str) -> 'CopyProductRulesCustomFieldListLoadQuery':
		"""
		Set CopyProductRules_Name.

		:param copy_product_rules_name: str
		:returns: CopyProductRulesCustomFieldListLoadQuery
		"""

		self.copy_product_rules_name = copy_product_rules_name
		return self

	def set_assigned(self, assigned: bool) -> 'CopyProductRulesCustomFieldListLoadQuery':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CopyProductRulesCustomFieldListLoadQuery
		"""

		self.assigned = assigned
		return self

	def set_unassigned(self, unassigned: bool) -> 'CopyProductRulesCustomFieldListLoadQuery':
		"""
		Set Unassigned.

		:param unassigned: bool
		:returns: CopyProductRulesCustomFieldListLoadQuery
		"""

		self.unassigned = unassigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyProductRulesCustomFieldListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyProductRulesCustomFieldListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyProductRulesCustomFieldListLoadQuery(self, http_response, data)

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

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		if self.unassigned is not None:
			data['Unassigned'] = self.unassigned
		return data
