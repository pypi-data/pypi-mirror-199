"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Note data model.
"""

from merchantapi.abstract import Model

class Note(Model):
	def __init__(self, data: dict = None):
		"""
		Note Constructor

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

	def get_account_id(self) -> int:
		"""
		Get account_id.

		:returns: int
		"""

		return self.get_field('account_id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_note_text(self) -> str:
		"""
		Get notetext.

		:returns: string
		"""

		return self.get_field('notetext')

	def get_date_time_stamp(self) -> int:
		"""
		Get dtstamp.

		:returns: int
		"""

		return self.get_timestamp_field('dtstamp')

	def get_customer_login(self) -> str:
		"""
		Get cust_login.

		:returns: string
		"""

		return self.get_field('cust_login')

	def get_business_title(self) -> str:
		"""
		Get business_title.

		:returns: string
		"""

		return self.get_field('business_title')

	def get_admin_user(self) -> str:
		"""
		Get admin_user.

		:returns: string
		"""

		return self.get_field('admin_user')
