"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

VersionSettings data model.
"""

from merchantapi.abstract import Model

class VersionSettings(Model):
	def __init__(self, data: dict = None):
		"""
		VersionSettings Constructor

		:param data: dict
		"""

		self.data = data
	
	def is_scalar(self) -> bool:
		"""
		Check if the underlying data is a scalar value

		:returns: bool
		"""

		return not isinstance(self.data, dict) and not isinstance(self.data, list)

	def is_list(self) -> bool:
		"""
		Check if the underlying data is a list

		:returns: bool
		"""

		return isinstance(self.data, list)

	def is_dict(self) -> bool:
		"""
		Check if the underlying data is a dictionary

		:returns: bool
		"""

		return isinstance(self.data, dict)

	def has_item(self, item: str) -> bool:
		"""
		Check if an item exists in the dictionary

		:param item: {string}
		:returns: bool
		"""

		return self.is_dict() and item in self.data;
	
	def item_has_property(self, item: str, item_property: str) -> bool:
		"""
		Check if an item has a property

		:param item: {string}
		:param item_property: {string}
		:returns: bool
		"""
		
		if not self.is_dict() or not self.has_item(item):
			return False

		return item_property in self.data[item];

	def get_item(self, item: str):
		"""
		Get a items dictionary.

		:param item: str
		:returns: dict
		"""

		return self.data[item] if self.is_dict() and self.has_item(item) else None

	def get_item_property(self, item: str, item_property: str):
		"""
		Get a items dictionary.

		:param item: str
		:param item_property: str
		:returns: dict
		"""

		return self.data[item][item_property] if self.is_dict() and self.item_has_property(item, item_property) else None

	def get_data(self):
		"""
		Get the underlying data

		:returns: mixed
		"""

		return self.data

	def to_dict(self):
		"""
		Reduce the model to a dict.
		"""

		return self.data


	def set_item(self, item: str, value: dict) -> 'VersionSettings':
		"""
		Set a item settings dictionary

		:param item: str
		:param value: dict
		:returns: VersionSettings
		"""

		self[item] = value		
		return self

	def set_item_property(self, item: str, item_property: str, value) -> 'VersionSettings':
		"""
		Set a item property value for a specific item

		:param item: str
		:param item_property: str
		:param value: mixed
		:returns: VersionSettings
		"""

		if not self.has_item(item):
			self[item] = {}

		self[item][item_property] = value
