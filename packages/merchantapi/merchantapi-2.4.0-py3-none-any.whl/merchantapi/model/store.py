"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Store data model.
"""

from merchantapi.abstract import Model

class Store(Model):
	# CACHE_TYPE constants.
	CACHE_TYPE_NONE = 'none'
	CACHE_TYPE_REDIS = 'redis'

	def __init__(self, data: dict = None):
		"""
		Store Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_manager_id(self) -> int:
		"""
		Get manager_id.

		:returns: int
		"""

		return self.get_field('manager_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_license(self) -> str:
		"""
		Get license.

		:returns: string
		"""

		return self.get_field('license')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_owner(self) -> str:
		"""
		Get owner.

		:returns: string
		"""

		return self.get_field('owner')

	def get_email(self) -> str:
		"""
		Get email.

		:returns: string
		"""

		return self.get_field('email')

	def get_company(self) -> str:
		"""
		Get company.

		:returns: string
		"""

		return self.get_field('company')

	def get_address(self) -> str:
		"""
		Get address.

		:returns: string
		"""

		return self.get_field('address')

	def get_city(self) -> str:
		"""
		Get city.

		:returns: string
		"""

		return self.get_field('city')

	def get_state(self) -> str:
		"""
		Get state.

		:returns: string
		"""

		return self.get_field('state')

	def get_zip(self) -> str:
		"""
		Get zip.

		:returns: string
		"""

		return self.get_field('zip')

	def get_phone(self) -> str:
		"""
		Get phone.

		:returns: string
		"""

		return self.get_field('phone')

	def get_fax(self) -> str:
		"""
		Get fax.

		:returns: string
		"""

		return self.get_field('fax')

	def get_country(self) -> str:
		"""
		Get country.

		:returns: string
		"""

		return self.get_field('country')

	def get_weight_units(self) -> str:
		"""
		Get wtunits.

		:returns: string
		"""

		return self.get_field('wtunits')

	def get_weight_unit_code(self) -> str:
		"""
		Get wtunitcode.

		:returns: string
		"""

		return self.get_field('wtunitcode')

	def get_dimension_units(self) -> str:
		"""
		Get dmunitcode.

		:returns: string
		"""

		return self.get_field('dmunitcode')

	def get_basket_expiration(self) -> int:
		"""
		Get baskexp.

		:returns: int
		"""

		return self.get_field('baskexp', 0)

	def get_price_group_overlap_resolution(self) -> str:
		"""
		Get pgrp_ovlp.

		:returns: string
		"""

		return self.get_field('pgrp_ovlp')

	def get_user_interface_id(self) -> int:
		"""
		Get ui_id.

		:returns: int
		"""

		return self.get_field('ui_id', 0)

	def get_tax_id(self) -> int:
		"""
		Get tax_id.

		:returns: int
		"""

		return self.get_field('tax_id', 0)

	def get_currency_id(self) -> int:
		"""
		Get currncy_id.

		:returns: int
		"""

		return self.get_field('currncy_id', 0)

	def get_maintenance_warning_message(self) -> str:
		"""
		Get mnt_warn.

		:returns: string
		"""

		return self.get_field('mnt_warn')

	def get_maintenance_closed_message(self) -> str:
		"""
		Get mnt_close.

		:returns: string
		"""

		return self.get_field('mnt_close')

	def get_maintenance_time(self) -> int:
		"""
		Get mnt_time.

		:returns: int
		"""

		return self.get_field('mnt_time', 0)

	def get_maintenance_no_new_customers_before(self) -> int:
		"""
		Get mnt_no_new.

		:returns: int
		"""

		return self.get_field('mnt_no_new', 0)

	def get_order_minimum_quantity(self) -> int:
		"""
		Get omin_quant.

		:returns: int
		"""

		return self.get_field('omin_quant', 0)

	def get_order_minimum_price(self) -> float:
		"""
		Get omin_price.

		:returns: float
		"""

		return self.get_field('omin_price', 0.00)

	def get_order_minimum_required_all(self) -> bool:
		"""
		Get omin_all.

		:returns: bool
		"""

		return self.get_field('omin_all', False)

	def get_order_minimum_message(self) -> str:
		"""
		Get omin_msg.

		:returns: string
		"""

		return self.get_field('omin_msg')

	def get_crypt_id(self) -> int:
		"""
		Get crypt_id.

		:returns: int
		"""

		return self.get_field('crypt_id', 0)

	def get_require_shipping(self) -> bool:
		"""
		Get req_ship.

		:returns: bool
		"""

		return self.get_field('req_ship', False)

	def get_require_tax(self) -> bool:
		"""
		Get req_tax.

		:returns: bool
		"""

		return self.get_field('req_tax', False)

	def get_require_free_order_shipping(self) -> bool:
		"""
		Get req_frship.

		:returns: bool
		"""

		return self.get_field('req_frship', False)

	def get_item_module_uninstallable(self) -> bool:
		"""
		Get item_adel.

		:returns: bool
		"""

		return self.get_field('item_adel', False)

	def get_cache_type(self) -> str:
		"""
		Get cache_type.

		:returns: string
		"""

		return self.get_field('cache_type')

	def get_redis_host(self) -> str:
		"""
		Get redishost.

		:returns: string
		"""

		return self.get_field('redishost')

	def get_redis_port(self) -> int:
		"""
		Get redisport.

		:returns: int
		"""

		return self.get_field('redisport', 0)

	def get_redis_timeout(self) -> int:
		"""
		Get redisto.

		:returns: int
		"""

		return self.get_field('redisto', 0)

	def get_redis_expiration(self) -> int:
		"""
		Get redisex.

		:returns: int
		"""

		return self.get_field('redisex', 0)
