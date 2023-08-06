"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

PaymentMethod data model.
"""

from merchantapi.abstract import Model
from .customer_payment_card import CustomerPaymentCard
from .order_payment_card import OrderPaymentCard
from .payment_card_type import PaymentCardType

class PaymentMethod(Model):
	def __init__(self, data: dict = None):
		"""
		PaymentMethod Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('paymentcard'):
			value = self.get_field('paymentcard')
			if isinstance(value, dict):
				if not isinstance(value, CustomerPaymentCard):
					self.set_field('paymentcard', CustomerPaymentCard(value))
			else:
				raise Exception('Expected CustomerPaymentCard or a dict')

		if self.has_field('orderpaymentcard'):
			value = self.get_field('orderpaymentcard')
			if isinstance(value, dict):
				if not isinstance(value, OrderPaymentCard):
					self.set_field('orderpaymentcard', OrderPaymentCard(value))
			else:
				raise Exception('Expected OrderPaymentCard or a dict')

		if self.has_field('paymentcardtype'):
			value = self.get_field('paymentcardtype')
			if isinstance(value, dict):
				if not isinstance(value, PaymentCardType):
					self.set_field('paymentcardtype', PaymentCardType(value))
			else:
				raise Exception('Expected PaymentCardType or a dict')

	def get_module_id(self) -> int:
		"""
		Get module_id.

		:returns: int
		"""

		return self.get_field('module_id', 0)

	def get_module_api(self) -> float:
		"""
		Get module_api.

		:returns: float
		"""

		return self.get_field('module_api', 0.00)

	def get_method_code(self) -> str:
		"""
		Get method_code.

		:returns: string
		"""

		return self.get_field('method_code')

	def get_method_name(self) -> str:
		"""
		Get method_name.

		:returns: string
		"""

		return self.get_field('method_name')

	def get_mivapay(self) -> bool:
		"""
		Get mivapay.

		:returns: bool
		"""

		return self.get_field('mivapay', False)

	def get_payment_card(self):
		"""
		Get paymentcard.

		:returns: CustomerPaymentCard|None
		"""

		return self.get_field('paymentcard', None)

	def get_order_payment_card(self):
		"""
		Get orderpaymentcard.

		:returns: OrderPaymentCard|None
		"""

		return self.get_field('orderpaymentcard', None)

	def get_payment_card_type(self):
		"""
		Get paymentcardtype.

		:returns: PaymentCardType|None
		"""

		return self.get_field('paymentcardtype', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'paymentcard' in ret and isinstance(ret['paymentcard'], CustomerPaymentCard):
			ret['paymentcard'] = ret['paymentcard'].to_dict()

		if 'orderpaymentcard' in ret and isinstance(ret['orderpaymentcard'], OrderPaymentCard):
			ret['orderpaymentcard'] = ret['orderpaymentcard'].to_dict()

		if 'paymentcardtype' in ret and isinstance(ret['paymentcardtype'], PaymentCardType):
			ret['paymentcardtype'] = ret['paymentcardtype'].to_dict()

		return ret
