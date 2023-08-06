"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Category data model.
"""

from merchantapi.abstract import Model
from .uri import Uri
from .custom_field_values import CustomFieldValues

class Category(Model):
	def __init__(self, data: dict = None):
		"""
		Category Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('uris'):
			value = self.get_field('uris')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Uri):
							value[i] = Uri(e)
					else:
						raise Exception('Expected list of Uri or dict')
			else:
				raise Exception('Expected list of Uri or dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_parent_id(self) -> int:
		"""
		Get parent_id.

		:returns: int
		"""

		return self.get_field('parent_id', 0)

	def get_availability_group_count(self) -> int:
		"""
		Get agrpcount.

		:returns: int
		"""

		return self.get_field('agrpcount', 0)

	def get_depth(self) -> int:
		"""
		Get depth.

		:returns: int
		"""

		return self.get_field('depth', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)

	def get_page_id(self) -> int:
		"""
		Get page_id.

		:returns: int
		"""

		return self.get_field('page_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_page_title(self) -> str:
		"""
		Get page_title.

		:returns: string
		"""

		return self.get_field('page_title')

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_timestamp_field('dt_created')

	def get_date_time_updated(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_timestamp_field('dt_updated')

	def get_page_code(self) -> str:
		"""
		Get page_code.

		:returns: string
		"""

		return self.get_field('page_code')

	def get_parent_category(self) -> str:
		"""
		Get parent_category.

		:returns: string
		"""

		return self.get_field('parent_category')

	def get_uris(self):
		"""
		Get uris.

		:returns: List of Uri
		"""

		return self.get_field('uris', [])

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'uris' in ret and isinstance(ret['uris'], list):
			for i, e in enumerate(ret['uris']):
				if isinstance(e, Uri):
					ret['uris'][i] = ret['uris'][i].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		return ret
