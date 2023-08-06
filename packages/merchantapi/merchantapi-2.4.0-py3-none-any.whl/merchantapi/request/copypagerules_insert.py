"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyPageRules_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copypagerules_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyPageRulesInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CopyPageRulesInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.name = None
		self.secure = None
		self.title = None
		self.template = None
		self.items = None
		self.settings = None
		self.javascript_resource_assignments = None
		self.css_resource_assignments = None
		self.cache_settings = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyPageRules_Insert'

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

	def set_name(self, name: str) -> 'CopyPageRulesInsert':
		"""
		Set Name.

		:param name: str
		:returns: CopyPageRulesInsert
		"""

		self.name = name
		return self

	def set_secure(self, secure: bool) -> 'CopyPageRulesInsert':
		"""
		Set Secure.

		:param secure: bool
		:returns: CopyPageRulesInsert
		"""

		self.secure = secure
		return self

	def set_title(self, title: bool) -> 'CopyPageRulesInsert':
		"""
		Set Title.

		:param title: bool
		:returns: CopyPageRulesInsert
		"""

		self.title = title
		return self

	def set_template(self, template: bool) -> 'CopyPageRulesInsert':
		"""
		Set Template.

		:param template: bool
		:returns: CopyPageRulesInsert
		"""

		self.template = template
		return self

	def set_items(self, items: bool) -> 'CopyPageRulesInsert':
		"""
		Set Items.

		:param items: bool
		:returns: CopyPageRulesInsert
		"""

		self.items = items
		return self

	def set_settings(self, settings: str) -> 'CopyPageRulesInsert':
		"""
		Set Settings.

		:param settings: str
		:returns: CopyPageRulesInsert
		"""

		self.settings = settings
		return self

	def set_javascript_resource_assignments(self, javascript_resource_assignments: bool) -> 'CopyPageRulesInsert':
		"""
		Set JavaScriptResourceAssignments.

		:param javascript_resource_assignments: bool
		:returns: CopyPageRulesInsert
		"""

		self.javascript_resource_assignments = javascript_resource_assignments
		return self

	def set_css_resource_assignments(self, css_resource_assignments: bool) -> 'CopyPageRulesInsert':
		"""
		Set CSSResourceAssignments.

		:param css_resource_assignments: bool
		:returns: CopyPageRulesInsert
		"""

		self.css_resource_assignments = css_resource_assignments
		return self

	def set_cache_settings(self, cache_settings: bool) -> 'CopyPageRulesInsert':
		"""
		Set CacheSettings.

		:param cache_settings: bool
		:returns: CopyPageRulesInsert
		"""

		self.cache_settings = cache_settings
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyPageRulesInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyPageRulesInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyPageRulesInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

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
