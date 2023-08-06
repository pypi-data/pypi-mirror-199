"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Product data model.
"""

from merchantapi.abstract import Model
from .product_inventory_settings import ProductInventorySettings
from .custom_field_values import CustomFieldValues
from .uri import Uri
from .related_product import RelatedProduct
from .category import Category
from .product_shipping_rules import ProductShippingRules
from .product_image_data import ProductImageData
from .product_attribute import ProductAttribute
from .product_subscription_settings import ProductSubscriptionSettings
from .product_subscription_term import ProductSubscriptionTerm

class Product(Model):
	def __init__(self, data: dict = None):
		"""
		Product Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('productinventorysettings'):
			value = self.get_field('productinventorysettings')
			if isinstance(value, dict):
				if not isinstance(value, ProductInventorySettings):
					self.set_field('productinventorysettings', ProductInventorySettings(value))
			else:
				raise Exception('Expected ProductInventorySettings or a dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

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

		if self.has_field('relatedproducts'):
			value = self.get_field('relatedproducts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, RelatedProduct):
							value[i] = RelatedProduct(e)
					else:
						raise Exception('Expected list of RelatedProduct or dict')
			else:
				raise Exception('Expected list of RelatedProduct or dict')

		if self.has_field('categories'):
			value = self.get_field('categories')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, Category):
							value[i] = Category(e)
					else:
						raise Exception('Expected list of Category or dict')
			else:
				raise Exception('Expected list of Category or dict')

		if self.has_field('productshippingrules'):
			value = self.get_field('productshippingrules')
			if isinstance(value, dict):
				if not isinstance(value, ProductShippingRules):
					self.set_field('productshippingrules', ProductShippingRules(value))
			else:
				raise Exception('Expected ProductShippingRules or a dict')

		if self.has_field('productimagedata'):
			value = self.get_field('productimagedata')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductImageData):
							value[i] = ProductImageData(e)
					else:
						raise Exception('Expected list of ProductImageData or dict')
			else:
				raise Exception('Expected list of ProductImageData or dict')

		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductAttribute):
							value[i] = ProductAttribute(e)
					else:
						raise Exception('Expected list of ProductAttribute or dict')
			else:
				raise Exception('Expected list of ProductAttribute or dict')

		if self.has_field('subscriptionsettings'):
			value = self.get_field('subscriptionsettings')
			if isinstance(value, dict):
				if not isinstance(value, ProductSubscriptionSettings):
					self.set_field('subscriptionsettings', ProductSubscriptionSettings(value))
			else:
				raise Exception('Expected ProductSubscriptionSettings or a dict')

		if self.has_field('subscriptionterms'):
			value = self.get_field('subscriptionterms')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductSubscriptionTerm):
							value[i] = ProductSubscriptionTerm(e)
					else:
						raise Exception('Expected list of ProductSubscriptionTerm or dict')
			else:
				raise Exception('Expected list of ProductSubscriptionTerm or dict')

		self['image_types'] = {}
		for (k,v) in self.items():
			if 'imagetype:' in k:
				self['image_types'][ k[ k.index(':')+1 : ] ] = v

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_thumbnail(self) -> str:
		"""
		Get thumbnail.

		:returns: string
		"""

		return self.get_field('thumbnail')

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_category_count(self) -> int:
		"""
		Get catcount.

		:returns: int
		"""

		return self.get_field('catcount', 0)

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_page_title(self) -> str:
		"""
		Get page_title.

		:returns: string
		"""

		return self.get_field('page_title')

	def get_taxable(self) -> bool:
		"""
		Get taxable.

		:returns: bool
		"""

		return self.get_field('taxable', False)

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_timestamp_field('dt_created')

	def get_date_time_update(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_timestamp_field('dt_updated')

	def get_product_inventory_settings(self):
		"""
		Get productinventorysettings.

		:returns: ProductInventorySettings|None
		"""

		return self.get_field('productinventorysettings', None)

	def get_product_inventory_active(self) -> bool:
		"""
		Get product_inventory_active.

		:returns: bool
		"""

		return self.get_field('product_inventory_active', False)

	def get_product_inventory(self) -> int:
		"""
		Get product_inventory.

		:returns: int
		"""

		return self.get_field('product_inventory', 0)

	def get_canonical_category_code(self) -> str:
		"""
		Get cancat_code.

		:returns: string
		"""

		return self.get_field('cancat_code')

	def get_page_code(self) -> str:
		"""
		Get page_code.

		:returns: string
		"""

		return self.get_field('page_code')

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def get_uris(self):
		"""
		Get uris.

		:returns: List of Uri
		"""

		return self.get_field('uris', [])

	def get_related_products(self):
		"""
		Get relatedproducts.

		:returns: List of RelatedProduct
		"""

		return self.get_field('relatedproducts', [])

	def get_categories(self):
		"""
		Get categories.

		:returns: List of Category
		"""

		return self.get_field('categories', [])

	def get_product_shipping_rules(self):
		"""
		Get productshippingrules.

		:returns: ProductShippingRules|None
		"""

		return self.get_field('productshippingrules', None)

	def get_product_image_data(self):
		"""
		Get productimagedata.

		:returns: List of ProductImageData
		"""

		return self.get_field('productimagedata', [])

	def get_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductAttribute
		"""

		return self.get_field('attributes', [])

	def get_url(self) -> str:
		"""
		Get url.

		:returns: string
		"""

		return self.get_field('url')

	def get_image_types(self) -> dict:
		"""
		Get imagetypes.

		:returns: dict
		"""

		return self.get_field('image_types', {})

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)

	def get_subscription_settings(self):
		"""
		Get subscriptionsettings.

		:returns: ProductSubscriptionSettings|None
		"""

		return self.get_field('subscriptionsettings', None)

	def get_subscription_terms(self):
		"""
		Get subscriptionterms.

		:returns: List of ProductSubscriptionTerm
		"""

		return self.get_field('subscriptionterms', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'productinventorysettings' in ret and isinstance(ret['productinventorysettings'], ProductInventorySettings):
			ret['productinventorysettings'] = ret['productinventorysettings'].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		if 'uris' in ret and isinstance(ret['uris'], list):
			for i, e in enumerate(ret['uris']):
				if isinstance(e, Uri):
					ret['uris'][i] = ret['uris'][i].to_dict()

		if 'relatedproducts' in ret and isinstance(ret['relatedproducts'], list):
			for i, e in enumerate(ret['relatedproducts']):
				if isinstance(e, RelatedProduct):
					ret['relatedproducts'][i] = ret['relatedproducts'][i].to_dict()

		if 'categories' in ret and isinstance(ret['categories'], list):
			for i, e in enumerate(ret['categories']):
				if isinstance(e, Category):
					ret['categories'][i] = ret['categories'][i].to_dict()

		if 'productshippingrules' in ret and isinstance(ret['productshippingrules'], ProductShippingRules):
			ret['productshippingrules'] = ret['productshippingrules'].to_dict()

		if 'productimagedata' in ret and isinstance(ret['productimagedata'], list):
			for i, e in enumerate(ret['productimagedata']):
				if isinstance(e, ProductImageData):
					ret['productimagedata'][i] = ret['productimagedata'][i].to_dict()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'subscriptionsettings' in ret and isinstance(ret['subscriptionsettings'], ProductSubscriptionSettings):
			ret['subscriptionsettings'] = ret['subscriptionsettings'].to_dict()

		if 'subscriptionterms' in ret and isinstance(ret['subscriptionterms'], list):
			for i, e in enumerate(ret['subscriptionterms']):
				if isinstance(e, ProductSubscriptionTerm):
					ret['subscriptionterms'][i] = ret['subscriptionterms'][i].to_dict()

		return ret
