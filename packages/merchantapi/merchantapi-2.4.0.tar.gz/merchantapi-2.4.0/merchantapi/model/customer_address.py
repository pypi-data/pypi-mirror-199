"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomerAddress data model.
"""

from merchantapi.abstract import Model

class CustomerAddress(Model):
	def __init__(self, data: dict = None):
		"""
		CustomerAddress Constructor

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

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

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

	def get_email(self) -> str:
		"""
		Get email.

		:returns: string
		"""

		return self.get_field('email')

	def get_company(self) -> str:
		"""
		Get comp.

		:returns: string
		"""

		return self.get_field('comp')

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

	def get_residential(self) -> bool:
		"""
		Get resdntl.

		:returns: bool
		"""

		return self.get_field('resdntl', False)
