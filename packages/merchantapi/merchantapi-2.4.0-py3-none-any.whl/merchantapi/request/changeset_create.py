"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Changeset_Create. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/changeset_create
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ChangesetCreate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, branch: merchantapi.model.Branch = None):
		"""
		ChangesetCreate Constructor.

		:param client: Client
		:param branch: Branch
		"""

		super().__init__(client)
		self.branch_id = None
		self.branch_name = None
		self.edit_branch = None
		self.notes = None
		self.tags = None
		self.template_changes = []
		self.resource_group_changes = []
		self.css_resource_changes = []
		self.javascript_resource_changes = []
		self.property_changes = []
		if isinstance(branch, merchantapi.model.Branch):
			if branch.get_id():
				self.set_branch_id(branch.get_id())

			self.set_branch_name(branch.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Changeset_Create'

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: str
		"""

		return self.notes

	def get_tags(self) -> str:
		"""
		Get Tags.

		:returns: str
		"""

		return self.tags

	def get_template_changes(self) -> list:
		"""
		Get Template_Changes.

		:returns: List of TemplateChange
		"""

		return self.template_changes

	def get_resource_group_changes(self) -> list:
		"""
		Get ResourceGroup_Changes.

		:returns: List of ResourceGroupChange
		"""

		return self.resource_group_changes

	def get_css_resource_changes(self) -> list:
		"""
		Get CSSResource_Changes.

		:returns: List of CSSResourceChange
		"""

		return self.css_resource_changes

	def get_javascript_resource_changes(self) -> list:
		"""
		Get JavaScriptResource_Changes.

		:returns: List of JavaScriptResourceChange
		"""

		return self.javascript_resource_changes

	def get_property_changes(self) -> list:
		"""
		Get Property_Changes.

		:returns: List of PropertyChange
		"""

		return self.property_changes

	def set_branch_id(self, branch_id: int) -> 'ChangesetCreate':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: ChangesetCreate
		"""

		self.branch_id = branch_id
		return self

	def set_branch_name(self, branch_name: str) -> 'ChangesetCreate':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: ChangesetCreate
		"""

		self.branch_name = branch_name
		return self

	def set_edit_branch(self, edit_branch: str) -> 'ChangesetCreate':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: ChangesetCreate
		"""

		self.edit_branch = edit_branch
		return self

	def set_notes(self, notes: str) -> 'ChangesetCreate':
		"""
		Set Notes.

		:param notes: str
		:returns: ChangesetCreate
		"""

		self.notes = notes
		return self

	def set_tags(self, tags: str) -> 'ChangesetCreate':
		"""
		Set Tags.

		:param tags: str
		:returns: ChangesetCreate
		"""

		self.tags = tags
		return self

	def set_template_changes(self, template_changes: list) -> 'ChangesetCreate':
		"""
		Set Template_Changes.

		:param template_changes: {TemplateChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in template_changes:
			if not isinstance(e, merchantapi.model.TemplateChange):
				raise Exception("")
		self.template_changes = template_changes
		return self

	def set_resource_group_changes(self, resource_group_changes: list) -> 'ChangesetCreate':
		"""
		Set ResourceGroup_Changes.

		:param resource_group_changes: {ResourceGroupChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in resource_group_changes:
			if not isinstance(e, merchantapi.model.ResourceGroupChange):
				raise Exception("")
		self.resource_group_changes = resource_group_changes
		return self

	def set_css_resource_changes(self, css_resource_changes: list) -> 'ChangesetCreate':
		"""
		Set CSSResource_Changes.

		:param css_resource_changes: {CSSResourceChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in css_resource_changes:
			if not isinstance(e, merchantapi.model.CSSResourceChange):
				raise Exception("")
		self.css_resource_changes = css_resource_changes
		return self

	def set_javascript_resource_changes(self, javascript_resource_changes: list) -> 'ChangesetCreate':
		"""
		Set JavaScriptResource_Changes.

		:param javascript_resource_changes: {JavaScriptResourceChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in javascript_resource_changes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceChange):
				raise Exception("")
		self.javascript_resource_changes = javascript_resource_changes
		return self

	def set_property_changes(self, property_changes: list) -> 'ChangesetCreate':
		"""
		Set Property_Changes.

		:param property_changes: {PropertyChange[]}
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in property_changes:
			if not isinstance(e, merchantapi.model.PropertyChange):
				raise Exception("")
		self.property_changes = property_changes
		return self
	
	def add_template_change(self, template_change) -> 'ChangesetCreate':
		"""
		Add Template_Changes.

		:param template_change: TemplateChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(template_change, merchantapi.model.TemplateChange):
			self.template_changes.append(template_change)
		elif isinstance(template_change, dict):
			self.template_changes.append(merchantapi.model.TemplateChange(template_change))
		else:
			raise Exception('Expected instance of TemplateChange or dict')
		return self

	def add_template_changes(self, template_changes: list) -> 'ChangesetCreate':
		"""
		Add many TemplateChange.

		:param template_changes: List of TemplateChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in template_changes:
			if not isinstance(e, merchantapi.model.TemplateChange):
				raise Exception('')
			self.template_changes.append(e)

		return self
	
	def add_resource_group_change(self, resource_group_change) -> 'ChangesetCreate':
		"""
		Add ResourceGroup_Changes.

		:param resource_group_change: ResourceGroupChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(resource_group_change, merchantapi.model.ResourceGroupChange):
			self.resource_group_changes.append(resource_group_change)
		elif isinstance(resource_group_change, dict):
			self.resource_group_changes.append(merchantapi.model.ResourceGroupChange(resource_group_change))
		else:
			raise Exception('Expected instance of ResourceGroupChange or dict')
		return self

	def add_resource_group_changes(self, resource_group_changes: list) -> 'ChangesetCreate':
		"""
		Add many ResourceGroupChange.

		:param resource_group_changes: List of ResourceGroupChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in resource_group_changes:
			if not isinstance(e, merchantapi.model.ResourceGroupChange):
				raise Exception('')
			self.resource_group_changes.append(e)

		return self
	
	def add_css_resource_change(self, css_resource_change) -> 'ChangesetCreate':
		"""
		Add CSSResource_Changes.

		:param css_resource_change: CSSResourceChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(css_resource_change, merchantapi.model.CSSResourceChange):
			self.css_resource_changes.append(css_resource_change)
		elif isinstance(css_resource_change, dict):
			self.css_resource_changes.append(merchantapi.model.CSSResourceChange(css_resource_change))
		else:
			raise Exception('Expected instance of CSSResourceChange or dict')
		return self

	def add_css_resource_changes(self, css_resource_changes: list) -> 'ChangesetCreate':
		"""
		Add many CSSResourceChange.

		:param css_resource_changes: List of CSSResourceChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in css_resource_changes:
			if not isinstance(e, merchantapi.model.CSSResourceChange):
				raise Exception('')
			self.css_resource_changes.append(e)

		return self
	
	def add_javascript_resource_change(self, javascript_resource_change) -> 'ChangesetCreate':
		"""
		Add JavaScriptResource_Changes.

		:param javascript_resource_change: JavaScriptResourceChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(javascript_resource_change, merchantapi.model.JavaScriptResourceChange):
			self.javascript_resource_changes.append(javascript_resource_change)
		elif isinstance(javascript_resource_change, dict):
			self.javascript_resource_changes.append(merchantapi.model.JavaScriptResourceChange(javascript_resource_change))
		else:
			raise Exception('Expected instance of JavaScriptResourceChange or dict')
		return self

	def add_javascript_resource_changes(self, javascript_resource_changes: list) -> 'ChangesetCreate':
		"""
		Add many JavaScriptResourceChange.

		:param javascript_resource_changes: List of JavaScriptResourceChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in javascript_resource_changes:
			if not isinstance(e, merchantapi.model.JavaScriptResourceChange):
				raise Exception('')
			self.javascript_resource_changes.append(e)

		return self
	
	def add_property_change(self, property_change) -> 'ChangesetCreate':
		"""
		Add Property_Changes.

		:param property_change: PropertyChange 
		:raises Exception:
		:returns: {ChangesetCreate}
		"""

		if isinstance(property_change, merchantapi.model.PropertyChange):
			self.property_changes.append(property_change)
		elif isinstance(property_change, dict):
			self.property_changes.append(merchantapi.model.PropertyChange(property_change))
		else:
			raise Exception('Expected instance of PropertyChange or dict')
		return self

	def add_property_changes(self, property_changes: list) -> 'ChangesetCreate':
		"""
		Add many PropertyChange.

		:param property_changes: List of PropertyChange
		:raises Exception:
		:returns: ChangesetCreate
		"""

		for e in property_changes:
			if not isinstance(e, merchantapi.model.PropertyChange):
				raise Exception('')
			self.property_changes.append(e)

		return self
	
	def get_java_script_resource_changes(self) -> list:
		# Alias of get_javascript_resource_changes
		return self.get_javascript_resource_changes()

	def set_java_script_resource_changes(self, java_script_resource_changes: list) -> 'ChangesetCreate':
		# Alias of set_javascript_resource_changes
		return self.set_javascript_resource_changes(java_script_resource_changes)

	def add_java_script_resource_change(self, java_script_resource_change) -> 'ChangesetCreate':
		# Alias of add_javascript_resource_change
		return self.add_javascript_resource_change(java_script_resource_change)

	def add_java_script_resource_changes(self, java_script_resource_changes: list) -> 'ChangesetCreate':
		# Alias of add_javascript_resource_changes
		return self.add_javascript_resource_changes(java_script_resource_changes)

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ChangesetCreate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ChangesetCreate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ChangesetCreate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch

		if self.branch_name is not None:
			data['Branch_Name'] = self.branch_name
		if self.notes is not None:
			data['Notes'] = self.notes
		if self.tags is not None:
			data['Tags'] = self.tags
		if len(self.template_changes):
			data['Template_Changes'] = []

			for f in self.template_changes:
				data['Template_Changes'].append(f.to_dict())
		if len(self.resource_group_changes):
			data['ResourceGroup_Changes'] = []

			for f in self.resource_group_changes:
				data['ResourceGroup_Changes'].append(f.to_dict())
		if len(self.css_resource_changes):
			data['CSSResource_Changes'] = []

			for f in self.css_resource_changes:
				data['CSSResource_Changes'].append(f.to_dict())
		if len(self.javascript_resource_changes):
			data['JavaScriptResource_Changes'] = []

			for f in self.javascript_resource_changes:
				data['JavaScriptResource_Changes'].append(f.to_dict())
		if len(self.property_changes):
			data['Property_Changes'] = []

			for f in self.property_changes:
				data['Property_Changes'].append(f.to_dict())
		return data
