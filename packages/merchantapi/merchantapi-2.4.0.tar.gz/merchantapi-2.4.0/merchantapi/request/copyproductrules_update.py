"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CopyProductRules_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/copyproductrules_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CopyProductRulesUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, copy_product_rule: merchantapi.model.CopyProductRule = None):
		"""
		CopyProductRulesUpdate Constructor.

		:param client: Client
		:param copy_product_rule: CopyProductRule
		"""

		super().__init__(client)
		self.copy_product_rules_id = None
		self.copy_product_rules_name = None
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
		if isinstance(copy_product_rule, merchantapi.model.CopyProductRule):
			if copy_product_rule.get_id():
				self.set_copy_product_rules_id(copy_product_rule.get_id())
			elif copy_product_rule.get_name():
				self.set_copy_product_rules_name(copy_product_rule.get_name())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CopyProductRules_Update'

	def get_copy_product_rules_id(self) -> int:
		"""
		Get CopyProductRules_ID.

		:returns: int
		"""

		return self.copy_product_rules_id

	def get_copy_product_rules_name(self) -> str:
		"""
		Get CopyProductRules_Name.

		:returns: str
		"""

		return self.copy_product_rules_name

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

	def set_copy_product_rules_id(self, copy_product_rules_id: int) -> 'CopyProductRulesUpdate':
		"""
		Set CopyProductRules_ID.

		:param copy_product_rules_id: int
		:returns: CopyProductRulesUpdate
		"""

		self.copy_product_rules_id = copy_product_rules_id
		return self

	def set_copy_product_rules_name(self, copy_product_rules_name: str) -> 'CopyProductRulesUpdate':
		"""
		Set CopyProductRules_Name.

		:param copy_product_rules_name: str
		:returns: CopyProductRulesUpdate
		"""

		self.copy_product_rules_name = copy_product_rules_name
		return self

	def set_name(self, name: str) -> 'CopyProductRulesUpdate':
		"""
		Set Name.

		:param name: str
		:returns: CopyProductRulesUpdate
		"""

		self.name = name
		return self

	def set_core_product_data(self, core_product_data: bool) -> 'CopyProductRulesUpdate':
		"""
		Set CoreProductData.

		:param core_product_data: bool
		:returns: CopyProductRulesUpdate
		"""

		self.core_product_data = core_product_data
		return self

	def set_attributes(self, attributes: bool) -> 'CopyProductRulesUpdate':
		"""
		Set Attributes.

		:param attributes: bool
		:returns: CopyProductRulesUpdate
		"""

		self.attributes = attributes
		return self

	def set_category_assignments(self, category_assignments: bool) -> 'CopyProductRulesUpdate':
		"""
		Set CategoryAssignments.

		:param category_assignments: bool
		:returns: CopyProductRulesUpdate
		"""

		self.category_assignments = category_assignments
		return self

	def set_inventory_settings(self, inventory_settings: bool) -> 'CopyProductRulesUpdate':
		"""
		Set InventorySettings.

		:param inventory_settings: bool
		:returns: CopyProductRulesUpdate
		"""

		self.inventory_settings = inventory_settings
		return self

	def set_inventory_level(self, inventory_level: bool) -> 'CopyProductRulesUpdate':
		"""
		Set InventoryLevel.

		:param inventory_level: bool
		:returns: CopyProductRulesUpdate
		"""

		self.inventory_level = inventory_level
		return self

	def set_images(self, images: bool) -> 'CopyProductRulesUpdate':
		"""
		Set Images.

		:param images: bool
		:returns: CopyProductRulesUpdate
		"""

		self.images = images
		return self

	def set_related_products(self, related_products: bool) -> 'CopyProductRulesUpdate':
		"""
		Set RelatedProducts.

		:param related_products: bool
		:returns: CopyProductRulesUpdate
		"""

		self.related_products = related_products
		return self

	def set_upsale(self, upsale: bool) -> 'CopyProductRulesUpdate':
		"""
		Set Upsale.

		:param upsale: bool
		:returns: CopyProductRulesUpdate
		"""

		self.upsale = upsale
		return self

	def set_availability_group_assignments(self, availability_group_assignments: bool) -> 'CopyProductRulesUpdate':
		"""
		Set AvailabilityGroupAssignments.

		:param availability_group_assignments: bool
		:returns: CopyProductRulesUpdate
		"""

		self.availability_group_assignments = availability_group_assignments
		return self

	def set_price_group_assignments(self, price_group_assignments: bool) -> 'CopyProductRulesUpdate':
		"""
		Set PriceGroupAssignments.

		:param price_group_assignments: bool
		:returns: CopyProductRulesUpdate
		"""

		self.price_group_assignments = price_group_assignments
		return self

	def set_digital_download_settings(self, digital_download_settings: bool) -> 'CopyProductRulesUpdate':
		"""
		Set DigitalDownloadSettings.

		:param digital_download_settings: bool
		:returns: CopyProductRulesUpdate
		"""

		self.digital_download_settings = digital_download_settings
		return self

	def set_gift_certificate_sales(self, gift_certificate_sales: bool) -> 'CopyProductRulesUpdate':
		"""
		Set GiftCertificateSales.

		:param gift_certificate_sales: bool
		:returns: CopyProductRulesUpdate
		"""

		self.gift_certificate_sales = gift_certificate_sales
		return self

	def set_subscription_settings(self, subscription_settings: bool) -> 'CopyProductRulesUpdate':
		"""
		Set SubscriptionSettings.

		:param subscription_settings: bool
		:returns: CopyProductRulesUpdate
		"""

		self.subscription_settings = subscription_settings
		return self

	def set_payment_rules(self, payment_rules: bool) -> 'CopyProductRulesUpdate':
		"""
		Set PaymentRules.

		:param payment_rules: bool
		:returns: CopyProductRulesUpdate
		"""

		self.payment_rules = payment_rules
		return self

	def set_shipping_rules(self, shipping_rules: bool) -> 'CopyProductRulesUpdate':
		"""
		Set ShippingRules.

		:param shipping_rules: bool
		:returns: CopyProductRulesUpdate
		"""

		self.shipping_rules = shipping_rules
		return self

	def set_product_kits(self, product_kits: bool) -> 'CopyProductRulesUpdate':
		"""
		Set ProductKits.

		:param product_kits: bool
		:returns: CopyProductRulesUpdate
		"""

		self.product_kits = product_kits
		return self

	def set_product_variants(self, product_variants: bool) -> 'CopyProductRulesUpdate':
		"""
		Set ProductVariants.

		:param product_variants: bool
		:returns: CopyProductRulesUpdate
		"""

		self.product_variants = product_variants
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CopyProductRulesUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CopyProductRulesUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CopyProductRulesUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.copy_product_rules_id is not None:
			data['CopyProductRules_ID'] = self.copy_product_rules_id
		elif self.copy_product_rules_name is not None:
			data['CopyProductRules_Name'] = self.copy_product_rules_name

		if self.name is not None:
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
