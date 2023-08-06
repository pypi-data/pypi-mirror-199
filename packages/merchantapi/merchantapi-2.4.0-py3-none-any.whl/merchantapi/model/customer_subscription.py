"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomerSubscription data model.
"""

from .subscription import Subscription

class CustomerSubscription(Subscription):
	def __init__(self, data: dict = None):
		"""
		CustomerSubscription Constructor

		:param data: dict
		"""

		super().__init__(data)

		self['image_types'] = {}
		for (k,v) in self.items():
			if 'imagetype:' in k:
				self['image_types'][ k[ k.index(':')+1 : ] ] = v

	def get_frequency(self) -> str:
		"""
		Get frequency.

		:returns: string
		"""

		return self.get_field('frequency')

	def get_term(self) -> int:
		"""
		Get term.

		:returns: int
		"""

		return self.get_field('term', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_n(self) -> int:
		"""
		Get n.

		:returns: int
		"""

		return self.get_field('n', 0)

	def get_fixed_day_of_week(self) -> int:
		"""
		Get fixed_dow.

		:returns: int
		"""

		return self.get_field('fixed_dow', 0)

	def get_fixed_day_of_month(self) -> int:
		"""
		Get fixed_dom.

		:returns: int
		"""

		return self.get_field('fixed_dom', 0)

	def get_subscription_count(self) -> int:
		"""
		Get sub_count.

		:returns: int
		"""

		return self.get_field('sub_count', 0)

	def get_method(self) -> str:
		"""
		Get method.

		:returns: string
		"""

		return self.get_field('method')

	def get_product_code(self) -> str:
		"""
		Get product_code.

		:returns: string
		"""

		return self.get_field('product_code')

	def get_product_name(self) -> str:
		"""
		Get product_name.

		:returns: string
		"""

		return self.get_field('product_name')

	def get_product_sku(self) -> str:
		"""
		Get product_sku.

		:returns: string
		"""

		return self.get_field('product_sku')

	def get_product_price(self) -> float:
		"""
		Get product_price.

		:returns: float
		"""

		return self.get_field('product_price', 0.00)

	def get_product_formatted_price(self) -> str:
		"""
		Get product_formatted_price.

		:returns: string
		"""

		return self.get_field('product_formatted_price')

	def get_product_cost(self) -> float:
		"""
		Get product_cost.

		:returns: float
		"""

		return self.get_field('product_cost', 0.00)

	def get_product_formatted_cost(self) -> str:
		"""
		Get product_formatted_cost.

		:returns: string
		"""

		return self.get_field('product_formatted_cost')

	def get_product_weight(self) -> float:
		"""
		Get product_weight.

		:returns: float
		"""

		return self.get_field('product_weight', 0.00)

	def get_product_taxable(self) -> bool:
		"""
		Get product_taxable.

		:returns: bool
		"""

		return self.get_field('product_taxable', False)

	def get_product_thumbnail(self) -> str:
		"""
		Get product_thumbnail.

		:returns: string
		"""

		return self.get_field('product_thumbnail')

	def get_product_image(self) -> str:
		"""
		Get product_image.

		:returns: string
		"""

		return self.get_field('product_image')

	def get_product_active(self) -> bool:
		"""
		Get product_active.

		:returns: bool
		"""

		return self.get_field('product_active', False)

	def get_product_date_time_created(self) -> int:
		"""
		Get product_dt_created.

		:returns: int
		"""

		return self.get_timestamp_field('product_dt_created')

	def get_product_date_time_updated(self) -> int:
		"""
		Get product_dt_updated.

		:returns: int
		"""

		return self.get_timestamp_field('product_dt_updated')

	def get_product_page_title(self) -> str:
		"""
		Get product_page_title.

		:returns: string
		"""

		return self.get_field('product_page_title')

	def get_product_page_id(self) -> int:
		"""
		Get product_page_id.

		:returns: int
		"""

		return self.get_field('product_page_id', 0)

	def get_product_page_code(self) -> str:
		"""
		Get product_page_code.

		:returns: string
		"""

		return self.get_field('product_page_code')

	def get_product_canonical_category_id(self) -> int:
		"""
		Get product_cancat_id.

		:returns: int
		"""

		return self.get_field('product_cancat_id', 0)

	def get_product_canonical_category_code(self) -> str:
		"""
		Get product_cancat_code.

		:returns: string
		"""

		return self.get_field('product_cancat_code')

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

	def get_image_types(self) -> dict:
		"""
		Get imagetypes.

		:returns: dict
		"""

		return self.get_field('image_types', {})

	def get_payment_card_last_four(self) -> str:
		"""
		Get paymentcard_lastfour.

		:returns: string
		"""

		return self.get_field('paymentcard_lastfour')

	def get_payment_card_type(self) -> str:
		"""
		Get paymentcard_type.

		:returns: string
		"""

		return self.get_field('paymentcard_type')

	def get_address_description(self) -> str:
		"""
		Get address_descrip.

		:returns: string
		"""

		return self.get_field('address_descrip')

	def get_address_first_name(self) -> str:
		"""
		Get address_fname.

		:returns: string
		"""

		return self.get_field('address_fname')

	def get_address_last_name(self) -> str:
		"""
		Get address_lname.

		:returns: string
		"""

		return self.get_field('address_lname')

	def get_address_email(self) -> str:
		"""
		Get address_email.

		:returns: string
		"""

		return self.get_field('address_email')

	def get_address_company(self) -> str:
		"""
		Get address_comp.

		:returns: string
		"""

		return self.get_field('address_comp')

	def get_address_phone(self) -> str:
		"""
		Get address_phone.

		:returns: string
		"""

		return self.get_field('address_phone')

	def get_address_fax(self) -> str:
		"""
		Get address_fax.

		:returns: string
		"""

		return self.get_field('address_fax')

	def get_address_address(self) -> str:
		"""
		Get address_addr.

		:returns: string
		"""

		return self.get_field('address_addr')

	def get_address_address1(self) -> str:
		"""
		Get address_addr1.

		:returns: string
		"""

		return self.get_field('address_addr1')

	def get_address_address2(self) -> str:
		"""
		Get address_addr2.

		:returns: string
		"""

		return self.get_field('address_addr2')

	def get_address_city(self) -> str:
		"""
		Get address_city.

		:returns: string
		"""

		return self.get_field('address_city')

	def get_address_state(self) -> str:
		"""
		Get address_state.

		:returns: string
		"""

		return self.get_field('address_state')

	def get_address_zip(self) -> str:
		"""
		Get address_zip.

		:returns: string
		"""

		return self.get_field('address_zip')

	def get_address_country(self) -> str:
		"""
		Get address_cntry.

		:returns: string
		"""

		return self.get_field('address_cntry')

	def get_address_residential(self) -> bool:
		"""
		Get address_resdntl.

		:returns: bool
		"""

		return self.get_field('address_resdntl', False)

	def get_customer_login(self) -> str:
		"""
		Get customer_login.

		:returns: string
		"""

		return self.get_field('customer_login')

	def get_customer_password_email(self) -> str:
		"""
		Get customer_pw_email.

		:returns: string
		"""

		return self.get_field('customer_pw_email')

	def get_customer_business_title(self) -> str:
		"""
		Get customer_business_title.

		:returns: string
		"""

		return self.get_field('customer_business_title')
