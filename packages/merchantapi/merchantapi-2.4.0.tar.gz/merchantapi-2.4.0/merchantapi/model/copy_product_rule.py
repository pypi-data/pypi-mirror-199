"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CopyProductRule data model.
"""

from merchantapi.abstract import Model

class CopyProductRule(Model):
	def __init__(self, data: dict = None):
		"""
		CopyProductRule Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_core_product_data(self) -> bool:
		"""
		Get product.

		:returns: bool
		"""

		return self.get_field('product', False)

	def get_attributes(self) -> bool:
		"""
		Get attributes.

		:returns: bool
		"""

		return self.get_field('attributes', False)

	def get_category_assignments(self) -> bool:
		"""
		Get categories.

		:returns: bool
		"""

		return self.get_field('categories', False)

	def get_inventory_settings(self) -> bool:
		"""
		Get invset.

		:returns: bool
		"""

		return self.get_field('invset', False)

	def get_inventory_level(self) -> bool:
		"""
		Get invlevel.

		:returns: bool
		"""

		return self.get_field('invlevel', False)

	def get_images(self) -> bool:
		"""
		Get images.

		:returns: bool
		"""

		return self.get_field('images', False)

	def get_related_products(self) -> bool:
		"""
		Get relprod.

		:returns: bool
		"""

		return self.get_field('relprod', False)

	def get_upsale(self) -> bool:
		"""
		Get upsale.

		:returns: bool
		"""

		return self.get_field('upsale', False)

	def get_availability_group_assignments(self) -> bool:
		"""
		Get availgroup.

		:returns: bool
		"""

		return self.get_field('availgroup', False)

	def get_price_group_assignments(self) -> bool:
		"""
		Get pricegroup.

		:returns: bool
		"""

		return self.get_field('pricegroup', False)

	def get_digital_download_settings(self) -> bool:
		"""
		Get ddownload.

		:returns: bool
		"""

		return self.get_field('ddownload', False)

	def get_gift_certificate_sales(self) -> bool:
		"""
		Get giftcert.

		:returns: bool
		"""

		return self.get_field('giftcert', False)

	def get_subscription_settings(self) -> bool:
		"""
		Get subscrip.

		:returns: bool
		"""

		return self.get_field('subscrip', False)

	def get_payment_rules(self) -> bool:
		"""
		Get payment.

		:returns: bool
		"""

		return self.get_field('payment', False)

	def get_shipping_rules(self) -> bool:
		"""
		Get shipping.

		:returns: bool
		"""

		return self.get_field('shipping', False)

	def get_product_kits(self) -> bool:
		"""
		Get kit.

		:returns: bool
		"""

		return self.get_field('kit', False)

	def get_product_variants(self) -> bool:
		"""
		Get variants.

		:returns: bool
		"""

		return self.get_field('variants', False)
