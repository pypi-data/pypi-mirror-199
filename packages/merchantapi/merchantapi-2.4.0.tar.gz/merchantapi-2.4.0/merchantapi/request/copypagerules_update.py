"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyPageRules_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copypagerules_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyPageRulesUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, copy_page_rule: merchantapi.model.CopyPageRule = None):
		"""
		CopyPageRulesUpdate Constructor.

		:param client: Client
		:param copy_page_rule: CopyPageRule
		"""

		super().__init__(client)
		self.copy_page_rules_id = None
		self.copy_page_rules_name = None
		self.name = None
		self.secure = None
		self.title = None
		self.template = None
		self.items = None
		self.settings = None
		self.javascript_resource_assignments = None
		self.css_resource_assignments = None
		self.cache_settings = None
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

		return 'CopyPageRules_Update'

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

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_secure(self) -> bool:
		"""
		Get Secure.

		:returns: bool
		"""

		return self.secure

	def get_title(self) -> bool:
		"""
		Get Title.

		:returns: bool
		"""

		return self.title

	def get_template(self) -> bool:
		"""
		Get Template.

		:returns: bool
		"""

		return self.template

	def get_items(self) -> bool:
		"""
		Get Items.

		:returns: bool
		"""

		return self.items

	def get_settings(self) -> str:
		"""
		Get Settings.

		:returns: str
		"""

		return self.settings

	def get_javascript_resource_assignments(self) -> bool:
		"""
		Get JavaScriptResourceAssignments.

		:returns: bool
		"""

		return self.javascript_resource_assignments

	def get_css_resource_assignments(self) -> bool:
		"""
		Get CSSResourceAssignments.

		:returns: bool
		"""

		return self.css_resource_assignments

	def get_cache_settings(self) -> bool:
		"""
		Get CacheSettings.

		:returns: bool
		"""

		return self.cache_settings

	def set_copy_page_rules_id(self, copy_page_rules_id: int) -> 'CopyPageRulesUpdate':
		"""
		Set CopyPageRules_ID.

		:param copy_page_rules_id: int
		:returns: CopyPageRulesUpdate
		"""

		self.copy_page_rules_id = copy_page_rules_id
		return self

	def set_copy_page_rules_name(self, copy_page_rules_name: str) -> 'CopyPageRulesUpdate':
		"""
		Set CopyPageRules_Name.

		:param copy_page_rules_name: str
		:returns: CopyPageRulesUpdate
		"""

		self.copy_page_rules_name = copy_page_rules_name
		return self

	def set_name(self, name: str) -> 'CopyPageRulesUpdate':
		"""
		Set Name.

		:param name: str
		:returns: CopyPageRulesUpdate
		"""

		self.name = name
		return self

	def set_secure(self, secure: bool) -> 'CopyPageRulesUpdate':
		"""
		Set Secure.

		:param secure: bool
		:returns: CopyPageRulesUpdate
		"""

		self.secure = secure
		return self

	def set_title(self, title: bool) -> 'CopyPageRulesUpdate':
		"""
		Set Title.

		:param title: bool
		:returns: CopyPageRulesUpdate
		"""

		self.title = title
		return self

	def set_template(self, template: bool) -> 'CopyPageRulesUpdate':
		"""
		Set Template.

		:param template: bool
		:returns: CopyPageRulesUpdate
		"""

		self.template = template
		return self

	def set_items(self, items: bool) -> 'CopyPageRulesUpdate':
		"""
		Set Items.

		:param items: bool
		:returns: CopyPageRulesUpdate
		"""

		self.items = items
		return self

	def set_settings(self, settings: str) -> 'CopyPageRulesUpdate':
		"""
		Set Settings.

		:param settings: str
		:returns: CopyPageRulesUpdate
		"""

		self.settings = settings
		return self

	def set_javascript_resource_assignments(self, javascript_resource_assignments: bool) -> 'CopyPageRulesUpdate':
		"""
		Set JavaScriptResourceAssignments.

		:param javascript_resource_assignments: bool
		:returns: CopyPageRulesUpdate
		"""

		self.javascript_resource_assignments = javascript_resource_assignments
		return self

	def set_css_resource_assignments(self, css_resource_assignments: bool) -> 'CopyPageRulesUpdate':
		"""
		Set CSSResourceAssignments.

		:param css_resource_assignments: bool
		:returns: CopyPageRulesUpdate
		"""

		self.css_resource_assignments = css_resource_assignments
		return self

	def set_cache_settings(self, cache_settings: bool) -> 'CopyPageRulesUpdate':
		"""
		Set CacheSettings.

		:param cache_settings: bool
		:returns: CopyPageRulesUpdate
		"""

		self.cache_settings = cache_settings
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyPageRulesUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyPageRulesUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyPageRulesUpdate(self, http_response, data)

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

		if self.name is not None:
			data['Name'] = self.name
		if self.secure is not None:
			data['Secure'] = self.secure
		if self.title is not None:
			data['Title'] = self.title
		if self.template is not None:
			data['Template'] = self.template
		if self.items is not None:
			data['Items'] = self.items
		if self.settings is not None:
			data['Settings'] = self.settings
		if self.javascript_resource_assignments is not None:
			data['JavaScriptResourceAssignments'] = self.javascript_resource_assignments
		if self.css_resource_assignments is not None:
			data['CSSResourceAssignments'] = self.css_resource_assignments
		if self.cache_settings is not None:
			data['CacheSettings'] = self.cache_settings
		return data
