"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderCharge data model.
"""

from merchantapi.abstract import Model

class OrderCharge(Model):
	def __init__(self, data: dict = None):
		"""
		OrderCharge Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_charge_id(self) -> int:
		"""
		Get charge_id.

		:returns: int
		"""

		return self.get_field('charge_id', 0)

	def get_module_id(self) -> int:
		"""
		Get module_id.

		:returns: int
		"""

		return self.get_field('module_id', 0)

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_amount(self) -> float:
		"""
		Get amount.

		:returns: float
		"""

		return self.get_field('amount', 0.00)

	def get_formatted_amount(self) -> str:
		"""
		Get formatted_amount.

		:returns: string
		"""

		return self.get_field('formatted_amount')

	def get_display_amount(self) -> float:
		"""
		Get disp_amt.

		:returns: float
		"""

		return self.get_field('disp_amt', 0.00)

	def get_formatted_display_amount(self) -> str:
		"""
		Get formatted_disp_amt.

		:returns: string
		"""

		return self.get_field('formatted_disp_amt')

	def get_tax_exempt(self) -> bool:
		"""
		Get tax_exempt.

		:returns: bool
		"""

		return self.get_field('tax_exempt', False)

	def get_tax(self) -> float:
		"""
		Get tax.

		:returns: float
		"""

		return self.get_field('tax', 0.00)

	def get_formatted_tax(self) -> str:
		"""
		Get formatted_tax.

		:returns: string
		"""

		return self.get_field('formatted_tax')

	def set_type(self, type: str) -> 'OrderCharge':
		"""
		Set type.

		:param type: string
		:returns: OrderCharge
		"""

		return self.set_field('type', type)

	def set_description(self, description: str) -> 'OrderCharge':
		"""
		Set descrip.

		:param description: string
		:returns: OrderCharge
		"""

		return self.set_field('descrip', description)

	def set_amount(self, amount: float) -> 'OrderCharge':
		"""
		Set amount.

		:param amount: int
		:returns: OrderCharge
		"""

		return self.set_field('amount', amount)

	def set_display_amount(self, display_amount: float) -> 'OrderCharge':
		"""
		Set disp_amt.

		:param display_amount: int
		:returns: OrderCharge
		"""

		return self.set_field('disp_amt', display_amount)

	def set_tax_exempt(self, tax_exempt: bool) -> 'OrderCharge':
		"""
		Set tax_exempt.

		:param tax_exempt: bool
		:returns: OrderCharge
		"""

		return self.set_field('tax_exempt', tax_exempt)
