"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PropertyVersion data model.
"""

from merchantapi.abstract import Model
from .version_settings import VersionSettings
from .product import Product
from .category import Category

class PropertyVersion(Model):
	def __init__(self, data: dict = None):
		"""
		PropertyVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('settings'):
			value = self.get_field('settings')
			if not isinstance(value, VersionSettings):
				self.set_field('settings', VersionSettings(value))

		if self.has_field('product'):
			value = self.get_field('product')
			if isinstance(value, dict):
				if not isinstance(value, Product):
					self.set_field('product', Product(value))
			else:
				raise Exception('Expected Product or a dict')

		if self.has_field('category'):
			value = self.get_field('category')
			if isinstance(value, dict):
				if not isinstance(value, Category):
					self.set_field('category', Category(value))
			else:
				raise Exception('Expected Category or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_property_id(self) -> int:
		"""
		Get prop_id.

		:returns: int
		"""

		return self.get_field('prop_id', 0)

	def get_version_id(self) -> int:
		"""
		Get version_id.

		:returns: int
		"""

		return self.get_field('version_id', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_category_id(self) -> int:
		"""
		Get cat_id.

		:returns: int
		"""

		return self.get_field('cat_id', 0)

	def get_version_user_id(self) -> int:
		"""
		Get version_user_id.

		:returns: int
		"""

		return self.get_field('version_user_id', 0)

	def get_version_user_name(self) -> str:
		"""
		Get version_user_name.

		:returns: string
		"""

		return self.get_field('version_user_name')

	def get_version_user_icon(self) -> str:
		"""
		Get version_user_icon.

		:returns: string
		"""

		return self.get_field('version_user_icon')

	def get_source_user_id(self) -> int:
		"""
		Get source_user_id.

		:returns: int
		"""

		return self.get_field('source_user_id', 0)

	def get_source_user_name(self) -> str:
		"""
		Get source_user_name.

		:returns: string
		"""

		return self.get_field('source_user_name')

	def get_source_user_icon(self) -> str:
		"""
		Get source_user_icon.

		:returns: string
		"""

		return self.get_field('source_user_icon')

	def get_template_id(self) -> int:
		"""
		Get templ_id.

		:returns: int
		"""

		return self.get_field('templ_id', 0)

	def get_settings(self):
		"""
		Get settings.

		:returns: VersionSettings|None
		"""

		return self.get_field('settings', None)

	def get_product(self):
		"""
		Get product.

		:returns: Product|None
		"""

		return self.get_field('product', None)

	def get_category(self):
		"""
		Get category.

		:returns: Category|None
		"""

		return self.get_field('category', None)

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_sync(self) -> bool:
		"""
		Get sync.

		:returns: bool
		"""

		return self.get_field('sync', False)

	def get_source_notes(self) -> str:
		"""
		Get source_notes.

		:returns: string
		"""

		return self.get_field('source_notes')

	def get_image_id(self) -> int:
		"""
		Get image_id.

		:returns: int
		"""

		return self.get_field('image_id', 0)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_image_refcount(self) -> int:
		"""
		Get image_refcount.

		:returns: int
		"""

		return self.get_field('image_refcount', 0)

	def get_image_head_count(self) -> int:
		"""
		Get image_head_count.

		:returns: int
		"""

		return self.get_field('image_head_count', 0)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'settings' in ret and isinstance(ret['settings'], VersionSettings):
			ret['settings'] = ret['settings'].to_dict()

		if 'product' in ret and isinstance(ret['product'], Product):
			ret['product'] = ret['product'].to_dict()

		if 'category' in ret and isinstance(ret['category'], Category):
			ret['category'] = ret['category'].to_dict()

		return ret
