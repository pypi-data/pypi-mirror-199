"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomerPaymentCard data model.
"""

from merchantapi.abstract import Model

class CustomerPaymentCard(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerPaymentCard Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_first_name(self) -> str:
		"""
		Get fname.

		:returns: string
		"""

		return self.get_field('fname')

	def get_last_name(self) -> str:
		"""
		Get lname.

		:returns: string
		"""

		return self.get_field('lname')

	def get_expiration_month(self) -> int:
		"""
		Get exp_month.

		:returns: int
		"""

		return self.get_field('exp_month', 0)

	def get_expiration_year(self) -> int:
		"""
		Get exp_year.

		:returns: int
		"""

		return self.get_field('exp_year', 0)

	def get_last_four(self) -> str:
		"""
		Get lastfour.

		:returns: string
		"""

		return self.get_field('lastfour')

	def get_address1(self) -> str:
		"""
		Get addr1.

		:returns: string
		"""

		return self.get_field('addr1')

	def get_address2(self) -> str:
		"""
		Get addr2.

		:returns: string
		"""

		return self.get_field('addr2')

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

	def get_country(self) -> str:
		"""
		Get cntry.

		:returns: string
		"""

		return self.get_field('cntry')

	def get_last_used(self) -> str:
		"""
		Get lastused.

		:returns: string
		"""

		return self.get_field('lastused')

	def get_token(self) -> str:
		"""
		Get token.

		:returns: string
		"""

		return self.get_field('token')

	def get_type_id(self) -> int:
		"""
		Get type_id.

		:returns: int
		"""

		return self.get_field('type_id', 0)

	def get_reference_count(self) -> int:
		"""
		Get refcount.

		:returns: int
		"""

		return self.get_field('refcount', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_module_code(self) -> str:
		"""
		Get mod_code.

		:returns: string
		"""

		return self.get_field('mod_code')

	def get_method_code(self) -> str:
		"""
		Get meth_code.

		:returns: string
		"""

		return self.get_field('meth_code')
