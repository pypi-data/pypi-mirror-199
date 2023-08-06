"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PropertyChange data model.
"""

from merchantapi.abstract import Model
from .version_settings import VersionSettings

class PropertyChange(Model):
	def __init__(self, data: dict = None):
		"""
		PropertyChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Settings'):
			value = self.get_field('Settings')
			if not isinstance(value, VersionSettings):
				self.set_field('Settings', VersionSettings(value))

	def get_property_id(self) -> int:
		"""
		Get Property_ID.

		:returns: int
		"""

		return self.get_field('Property_ID', 0)

	def get_property_type(self) -> str:
		"""
		Get Property_Type.

		:returns: string
		"""

		return self.get_field('Property_Type')

	def get_property_code(self) -> str:
		"""
		Get Property_Code.

		:returns: string
		"""

		return self.get_field('Property_Code')

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.get_field('Product_ID', 0)

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: string
		"""

		return self.get_field('Product_Code')

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: string
		"""

		return self.get_field('Edit_Product')

	def get_category_id(self) -> int:
		"""
		Get Category_ID.

		:returns: int
		"""

		return self.get_field('Category_ID', 0)

	def get_category_code(self) -> str:
		"""
		Get Category_Code.

		:returns: string
		"""

		return self.get_field('Category_Code')

	def get_edit_category(self) -> str:
		"""
		Get Edit_Category.

		:returns: string
		"""

		return self.get_field('Edit_Category')

	def get_source(self) -> str:
		"""
		Get Source.

		:returns: string
		"""

		return self.get_field('Source')

	def get_settings(self):
		"""
		Get Settings.

		:returns: VersionSettings|None
		"""

		return self.get_field('Settings', None)

	def get_image(self) -> str:
		"""
		Get Image.

		:returns: string
		"""

		return self.get_field('Image')

	def get_image_id(self) -> int:
		"""
		Get Image_ID.

		:returns: int
		"""

		return self.get_field('Image_ID', 0)

	def get_notes(self) -> str:
		"""
		Get Notes.

		:returns: string
		"""

		return self.get_field('Notes')

	def set_property_id(self, property_id: int) -> 'PropertyChange':
		"""
		Set Property_ID.

		:param property_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Property_ID', property_id)

	def set_property_type(self, property_type: str) -> 'PropertyChange':
		"""
		Set Property_Type.

		:param property_type: string
		:returns: PropertyChange
		"""

		return self.set_field('Property_Type', property_type)

	def set_property_code(self, property_code: str) -> 'PropertyChange':
		"""
		Set Property_Code.

		:param property_code: string
		:returns: PropertyChange
		"""

		return self.set_field('Property_Code', property_code)

	def set_product_id(self, product_id: int) -> 'PropertyChange':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Product_ID', product_id)

	def set_product_code(self, product_code: str) -> 'PropertyChange':
		"""
		Set Product_Code.

		:param product_code: string
		:returns: PropertyChange
		"""

		return self.set_field('Product_Code', product_code)

	def set_edit_product(self, edit_product: str) -> 'PropertyChange':
		"""
		Set Edit_Product.

		:param edit_product: string
		:returns: PropertyChange
		"""

		return self.set_field('Edit_Product', edit_product)

	def set_category_id(self, category_id: int) -> 'PropertyChange':
		"""
		Set Category_ID.

		:param category_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Category_ID', category_id)

	def set_category_code(self, category_code: str) -> 'PropertyChange':
		"""
		Set Category_Code.

		:param category_code: string
		:returns: PropertyChange
		"""

		return self.set_field('Category_Code', category_code)

	def set_edit_category(self, edit_category: str) -> 'PropertyChange':
		"""
		Set Edit_Category.

		:param edit_category: string
		:returns: PropertyChange
		"""

		return self.set_field('Edit_Category', edit_category)

	def set_source(self, source: str) -> 'PropertyChange':
		"""
		Set Source.

		:param source: string
		:returns: PropertyChange
		"""

		return self.set_field('Source', source)

	def set_settings(self, settings) -> 'PropertyChange':
		"""
		Set Settings.

		:param settings: VersionSettings|dict
		:returns: PropertyChange
		:raises Exception:
		"""

		if settings is None or isinstance(settings, VersionSettings):
			return self.set_field('Settings', settings)
		return self.set_field('Settings', VersionSettings(settings))

	def set_image(self, image: str) -> 'PropertyChange':
		"""
		Set Image.

		:param image: string
		:returns: PropertyChange
		"""

		return self.set_field('Image', image)

	def set_image_id(self, image_id: int) -> 'PropertyChange':
		"""
		Set Image_ID.

		:param image_id: int
		:returns: PropertyChange
		"""

		return self.set_field('Image_ID', image_id)

	def set_notes(self, notes: str) -> 'PropertyChange':
		"""
		Set Notes.

		:param notes: string
		:returns: PropertyChange
		"""

		return self.set_field('Notes', notes)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Settings' in ret and isinstance(ret['Settings'], VersionSettings):
			ret['Settings'] = ret['Settings'].to_dict()

		return ret
