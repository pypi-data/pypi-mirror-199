"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ResourceGroupChange data model.
"""

from merchantapi.abstract import Model

class ResourceGroupChange(Model):
	def __init__(self, data: dict = None):
		"""
		ResourceGroupChange Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_resource_group_id(self) -> int:
		"""
		Get ResourceGroup_ID.

		:returns: int
		"""

		return self.get_field('ResourceGroup_ID', 0)

	def get_resource_group_code(self) -> str:
		"""
		Get ResourceGroup_Code.

		:returns: string
		"""

		return self.get_field('ResourceGroup_Code')

	def get_linked_css_resources(self) -> dict:
		"""
		Get LinkedCSSResources.

		:returns: dict
		"""

		return self.get_field('LinkedCSSResources', {})

	def get_linked_javascript_resources(self) -> dict:
		"""
		Get LinkedJavaScriptResources.

		:returns: dict
		"""

		return self.get_field('LinkedJavaScriptResources', {})

	def set_resource_group_id(self, resource_group_id: int) -> 'ResourceGroupChange':
		"""
		Set ResourceGroup_ID.

		:param resource_group_id: int
		:returns: ResourceGroupChange
		"""

		return self.set_field('ResourceGroup_ID', resource_group_id)

	def set_resource_group_code(self, resource_group_code: str) -> 'ResourceGroupChange':
		"""
		Set ResourceGroup_Code.

		:param resource_group_code: string
		:returns: ResourceGroupChange
		"""

		return self.set_field('ResourceGroup_Code', resource_group_code)

	def set_linked_css_resources(self, linked_css_resources) -> 'ResourceGroupChange':
		"""
		Set LinkedCSSResources.

		:param linked_css_resources: list
		:returns: ResourceGroupChange
		"""

		return self.set_field('LinkedCSSResources', linked_css_resources)

	def set_linked_javascript_resources(self, linked_javascript_resources) -> 'ResourceGroupChange':
		"""
		Set LinkedJavaScriptResources.

		:param linked_javascript_resources: list
		:returns: ResourceGroupChange
		"""

		return self.set_field('LinkedJavaScriptResources', linked_javascript_resources)

	def get_linked_java_script_resources(self) -> dict:
		# Alias of get_linked_javascript_resources
		return self.get_linked_javascript_resources()

	def set_linked_java_script_resources(self, linked_java_script_resources) -> 'ResourceGroupChange':
		# Alias of set_linked_javascript_resources
		return self.set_linked_javascript_resources(linked_java_script_resources)
