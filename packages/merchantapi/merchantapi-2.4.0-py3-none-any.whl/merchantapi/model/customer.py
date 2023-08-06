"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Customer data model.
"""

from merchantapi.abstract import Model
from .custom_field_values import CustomFieldValues

class Customer(Model):
	def __init__(self, data: dict = None):
		"""
		Customer Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_account_id(self) -> int:
		"""
		Get account_id.

		:returns: int
		"""

		return self.get_field('account_id', 0)

	def get_login(self) -> str:
		"""
		Get login.

		:returns: string
		"""

		return self.get_field('login')

	def get_password_email(self) -> str:
		"""
		Get pw_email.

		:returns: string
		"""

		return self.get_field('pw_email')

	def get_ship_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_shipping_residential(self) -> bool:
		"""
		Get ship_res.

		:returns: bool
		"""

		return self.get_field('ship_res', False)

	def get_ship_first_name(self) -> str:
		"""
		Get ship_fname.

		:returns: string
		"""

		return self.get_field('ship_fname')

	def get_ship_last_name(self) -> str:
		"""
		Get ship_lname.

		:returns: string
		"""

		return self.get_field('ship_lname')

	def get_ship_email(self) -> str:
		"""
		Get ship_email.

		:returns: string
		"""

		return self.get_field('ship_email')

	def get_ship_company(self) -> str:
		"""
		Get ship_comp.

		:returns: string
		"""

		return self.get_field('ship_comp')

	def get_ship_phone(self) -> str:
		"""
		Get ship_phone.

		:returns: string
		"""

		return self.get_field('ship_phone')

	def get_ship_fax(self) -> str:
		"""
		Get ship_fax.

		:returns: string
		"""

		return self.get_field('ship_fax')

	def get_ship_address1(self) -> str:
		"""
		Get ship_addr1.

		:returns: string
		"""

		return self.get_field('ship_addr1')

	def get_ship_address2(self) -> str:
		"""
		Get ship_addr2.

		:returns: string
		"""

		return self.get_field('ship_addr2')

	def get_ship_city(self) -> str:
		"""
		Get ship_city.

		:returns: string
		"""

		return self.get_field('ship_city')

	def get_ship_state(self) -> str:
		"""
		Get ship_state.

		:returns: string
		"""

		return self.get_field('ship_state')

	def get_ship_zip(self) -> str:
		"""
		Get ship_zip.

		:returns: string
		"""

		return self.get_field('ship_zip')

	def get_ship_country(self) -> str:
		"""
		Get ship_cntry.

		:returns: string
		"""

		return self.get_field('ship_cntry')

	def get_bill_id(self) -> int:
		"""
		Get bill_id.

		:returns: int
		"""

		return self.get_field('bill_id', 0)

	def get_bill_first_name(self) -> str:
		"""
		Get bill_fname.

		:returns: string
		"""

		return self.get_field('bill_fname')

	def get_bill_last_name(self) -> str:
		"""
		Get bill_lname.

		:returns: string
		"""

		return self.get_field('bill_lname')

	def get_bill_email(self) -> str:
		"""
		Get bill_email.

		:returns: string
		"""

		return self.get_field('bill_email')

	def get_bill_company(self) -> str:
		"""
		Get bill_comp.

		:returns: string
		"""

		return self.get_field('bill_comp')

	def get_bill_phone(self) -> str:
		"""
		Get bill_phone.

		:returns: string
		"""

		return self.get_field('bill_phone')

	def get_bill_fax(self) -> str:
		"""
		Get bill_fax.

		:returns: string
		"""

		return self.get_field('bill_fax')

	def get_bill_address1(self) -> str:
		"""
		Get bill_addr1.

		:returns: string
		"""

		return self.get_field('bill_addr1')

	def get_bill_address2(self) -> str:
		"""
		Get bill_addr2.

		:returns: string
		"""

		return self.get_field('bill_addr2')

	def get_bill_city(self) -> str:
		"""
		Get bill_city.

		:returns: string
		"""

		return self.get_field('bill_city')

	def get_bill_state(self) -> str:
		"""
		Get bill_state.

		:returns: string
		"""

		return self.get_field('bill_state')

	def get_bill_zip(self) -> str:
		"""
		Get bill_zip.

		:returns: string
		"""

		return self.get_field('bill_zip')

	def get_bill_country(self) -> str:
		"""
		Get bill_cntry.

		:returns: string
		"""

		return self.get_field('bill_cntry')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)

	def get_order_count(self) -> int:
		"""
		Get order_cnt.

		:returns: int
		"""

		return self.get_field('order_cnt', 0)

	def get_order_average(self) -> float:
		"""
		Get order_avg.

		:returns: float
		"""

		return self.get_field('order_avg', 0.00)

	def get_formatted_order_average(self) -> str:
		"""
		Get formatted_order_avg.

		:returns: string
		"""

		return self.get_field('formatted_order_avg')

	def get_order_total(self) -> float:
		"""
		Get order_tot.

		:returns: float
		"""

		return self.get_field('order_tot', 0.00)

	def get_formatted_order_total(self) -> str:
		"""
		Get formatted_order_tot.

		:returns: string
		"""

		return self.get_field('formatted_order_tot')

	def get_note_count(self) -> int:
		"""
		Get note_count.

		:returns: int
		"""

		return self.get_field('note_count', 0)

	def get_created_on(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_timestamp_field('dt_created')

	def get_last_login(self) -> int:
		"""
		Get dt_login.

		:returns: int
		"""

		return self.get_timestamp_field('dt_login')

	def get_password_change_date_time(self) -> int:
		"""
		Get dt_pwchg.

		:returns: int
		"""

		return self.get_timestamp_field('dt_pwchg')

	def get_credit(self) -> float:
		"""
		Get credit.

		:returns: float
		"""

		return self.get_field('credit', 0.00)

	def get_formatted_credit(self) -> str:
		"""
		Get formatted_credit.

		:returns: string
		"""

		return self.get_field('formatted_credit')

	def get_business_title(self) -> str:
		"""
		Get business_title.

		:returns: string
		"""

		return self.get_field('business_title')

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		return ret
