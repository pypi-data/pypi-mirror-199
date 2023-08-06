"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyProductRules_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copyproductrules_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyProductRulesInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		CopyProductRulesInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.name = None
		self.core_product_data = None
		self.attributes = None
		self.category_assignments = None
		self.inventory_settings = None
		self.inventory_level = None
		self.images = None
		self.related_products = None
		self.upsale = None
		self.availability_group_assignments = None
		self.price_group_assignments = None
		self.digital_download_settings = None
		self.gift_certificate_sales = None
		self.subscription_settings = None
		self.payment_rules = None
		self.shipping_rules = None
		self.product_kits = None
		self.product_variants = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyProductRules_Insert'

	def get_name(self) -> str:
		"""
		Get Name.

		:returns: str
		"""

		return self.name

	def get_core_product_data(self) -> bool:
		"""
		Get CoreProductData.

		:returns: bool
		"""

		return self.core_product_data

	def get_attributes(self) -> bool:
		"""
		Get Attributes.

		:returns: bool
		"""

		return self.attributes

	def get_category_assignments(self) -> bool:
		"""
		Get CategoryAssignments.

		:returns: bool
		"""

		return self.category_assignments

	def get_inventory_settings(self) -> bool:
		"""
		Get InventorySettings.

		:returns: bool
		"""

		return self.inventory_settings

	def get_inventory_level(self) -> bool:
		"""
		Get InventoryLevel.

		:returns: bool
		"""

		return self.inventory_level

	def get_images(self) -> bool:
		"""
		Get Images.

		:returns: bool
		"""

		return self.images

	def get_related_products(self) -> bool:
		"""
		Get RelatedProducts.

		:returns: bool
		"""

		return self.related_products

	def get_upsale(self) -> bool:
		"""
		Get Upsale.

		:returns: bool
		"""

		return self.upsale

	def get_availability_group_assignments(self) -> bool:
		"""
		Get AvailabilityGroupAssignments.

		:returns: bool
		"""

		return self.availability_group_assignments

	def get_price_group_assignments(self) -> bool:
		"""
		Get PriceGroupAssignments.

		:returns: bool
		"""

		return self.price_group_assignments

	def get_digital_download_settings(self) -> bool:
		"""
		Get DigitalDownloadSettings.

		:returns: bool
		"""

		return self.digital_download_settings

	def get_gift_certificate_sales(self) -> bool:
		"""
		Get GiftCertificateSales.

		:returns: bool
		"""

		return self.gift_certificate_sales

	def get_subscription_settings(self) -> bool:
		"""
		Get SubscriptionSettings.

		:returns: bool
		"""

		return self.subscription_settings

	def get_payment_rules(self) -> bool:
		"""
		Get PaymentRules.

		:returns: bool
		"""

		return self.payment_rules

	def get_shipping_rules(self) -> bool:
		"""
		Get ShippingRules.

		:returns: bool
		"""

		return self.shipping_rules

	def get_product_kits(self) -> bool:
		"""
		Get ProductKits.

		:returns: bool
		"""

		return self.product_kits

	def get_product_variants(self) -> bool:
		"""
		Get ProductVariants.

		:returns: bool
		"""

		return self.product_variants

	def set_name(self, name: str) -> 'CopyProductRulesInsert':
		"""
		Set Name.

		:param name: str
		:returns: CopyProductRulesInsert
		"""

		self.name = name
		return self

	def set_core_product_data(self, core_product_data: bool) -> 'CopyProductRulesInsert':
		"""
		Set CoreProductData.

		:param core_product_data: bool
		:returns: CopyProductRulesInsert
		"""

		self.core_product_data = core_product_data
		return self

	def set_attributes(self, attributes: bool) -> 'CopyProductRulesInsert':
		"""
		Set Attributes.

		:param attributes: bool
		:returns: CopyProductRulesInsert
		"""

		self.attributes = attributes
		return self

	def set_category_assignments(self, category_assignments: bool) -> 'CopyProductRulesInsert':
		"""
		Set CategoryAssignments.

		:param category_assignments: bool
		:returns: CopyProductRulesInsert
		"""

		self.category_assignments = category_assignments
		return self

	def set_inventory_settings(self, inventory_settings: bool) -> 'CopyProductRulesInsert':
		"""
		Set InventorySettings.

		:param inventory_settings: bool
		:returns: CopyProductRulesInsert
		"""

		self.inventory_settings = inventory_settings
		return self

	def set_inventory_level(self, inventory_level: bool) -> 'CopyProductRulesInsert':
		"""
		Set InventoryLevel.

		:param inventory_level: bool
		:returns: CopyProductRulesInsert
		"""

		self.inventory_level = inventory_level
		return self

	def set_images(self, images: bool) -> 'CopyProductRulesInsert':
		"""
		Set Images.

		:param images: bool
		:returns: CopyProductRulesInsert
		"""

		self.images = images
		return self

	def set_related_products(self, related_products: bool) -> 'CopyProductRulesInsert':
		"""
		Set RelatedProducts.

		:param related_products: bool
		:returns: CopyProductRulesInsert
		"""

		self.related_products = related_products
		return self

	def set_upsale(self, upsale: bool) -> 'CopyProductRulesInsert':
		"""
		Set Upsale.

		:param upsale: bool
		:returns: CopyProductRulesInsert
		"""

		self.upsale = upsale
		return self

	def set_availability_group_assignments(self, availability_group_assignments: bool) -> 'CopyProductRulesInsert':
		"""
		Set AvailabilityGroupAssignments.

		:param availability_group_assignments: bool
		:returns: CopyProductRulesInsert
		"""

		self.availability_group_assignments = availability_group_assignments
		return self

	def set_price_group_assignments(self, price_group_assignments: bool) -> 'CopyProductRulesInsert':
		"""
		Set PriceGroupAssignments.

		:param price_group_assignments: bool
		:returns: CopyProductRulesInsert
		"""

		self.price_group_assignments = price_group_assignments
		return self

	def set_digital_download_settings(self, digital_download_settings: bool) -> 'CopyProductRulesInsert':
		"""
		Set DigitalDownloadSettings.

		:param digital_download_settings: bool
		:returns: CopyProductRulesInsert
		"""

		self.digital_download_settings = digital_download_settings
		return self

	def set_gift_certificate_sales(self, gift_certificate_sales: bool) -> 'CopyProductRulesInsert':
		"""
		Set GiftCertificateSales.

		:param gift_certificate_sales: bool
		:returns: CopyProductRulesInsert
		"""

		self.gift_certificate_sales = gift_certificate_sales
		return self

	def set_subscription_settings(self, subscription_settings: bool) -> 'CopyProductRulesInsert':
		"""
		Set SubscriptionSettings.

		:param subscription_settings: bool
		:returns: CopyProductRulesInsert
		"""

		self.subscription_settings = subscription_settings
		return self

	def set_payment_rules(self, payment_rules: bool) -> 'CopyProductRulesInsert':
		"""
		Set PaymentRules.

		:param payment_rules: bool
		:returns: CopyProductRulesInsert
		"""

		self.payment_rules = payment_rules
		return self

	def set_shipping_rules(self, shipping_rules: bool) -> 'CopyProductRulesInsert':
		"""
		Set ShippingRules.

		:param shipping_rules: bool
		:returns: CopyProductRulesInsert
		"""

		self.shipping_rules = shipping_rules
		return self

	def set_product_kits(self, product_kits: bool) -> 'CopyProductRulesInsert':
		"""
		Set ProductKits.

		:param product_kits: bool
		:returns: CopyProductRulesInsert
		"""

		self.product_kits = product_kits
		return self

	def set_product_variants(self, product_variants: bool) -> 'CopyProductRulesInsert':
		"""
		Set ProductVariants.

		:param product_variants: bool
		:returns: CopyProductRulesInsert
		"""

		self.product_variants = product_variants
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyProductRulesInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyProductRulesInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyProductRulesInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Name'] = self.name
		if self.core_product_data is not None:
			data['CoreProductData'] = self.core_product_data
		if self.attributes is not None:
			data['Attributes'] = self.attributes
		if self.category_assignments is not None:
			data['CategoryAssignments'] = self.category_assignments
		if self.inventory_settings is not None:
			data['InventorySettings'] = self.inventory_settings
		if self.inventory_level is not None:
			data['InventoryLevel'] = self.inventory_level
		if self.images is not None:
			data['Images'] = self.images
		if self.related_products is not None:
			data['RelatedProducts'] = self.related_products
		if self.upsale is not None:
			data['Upsale'] = self.upsale
		if self.availability_group_assignments is not None:
			data['AvailabilityGroupAssignments'] = self.availability_group_assignments
		if self.price_group_assignments is not None:
			data['PriceGroupAssignments'] = self.price_group_assignments
		if self.digital_download_settings is not None:
			data['DigitalDownloadSettings'] = self.digital_download_settings
		if self.gift_certificate_sales is not None:
			data['GiftCertificateSales'] = self.gift_certificate_sales
		if self.subscription_settings is not None:
			data['SubscriptionSettings'] = self.subscription_settings
		if self.payment_rules is not None:
			data['PaymentRules'] = self.payment_rules
		if self.shipping_rules is not None:
			data['ShippingRules'] = self.shipping_rules
		if self.product_kits is not None:
			data['ProductKits'] = self.product_kits
		if self.product_variants is not None:
			data['ProductVariants'] = self.product_variants
		return data
