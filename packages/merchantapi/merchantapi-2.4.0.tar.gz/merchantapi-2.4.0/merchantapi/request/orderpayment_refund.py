"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderPayment_Refund. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderpayment_refund
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderPaymentRefund(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, order_payment: merchantapi.model.OrderPayment = None):
		"""
		OrderPaymentRefund Constructor.

		:param client: Client
		:param order_payment: OrderPayment
		"""

		super().__init__(client)
		self.order_payment_id = None
		self.amount = None
		if isinstance(order_payment, merchantapi.model.OrderPayment):
			self.set_order_payment_id(order_payment.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderPayment_Refund'

	def get_order_payment_id(self) -> int:
		"""
		Get OrderPayment_ID.

		:returns: int
		"""

		return self.order_payment_id

	def get_amount(self) -> float:
		"""
		Get Amount.

		:returns: float
		"""

		return self.amount

	def set_order_payment_id(self, order_payment_id: int) -> 'OrderPaymentRefund':
		"""
		Set OrderPayment_ID.

		:param order_payment_id: int
		:returns: OrderPaymentRefund
		"""

		self.order_payment_id = order_payment_id
		return self

	def set_amount(self, amount: float) -> 'OrderPaymentRefund':
		"""
		Set Amount.

		:param amount: float
		:returns: OrderPaymentRefund
		"""

		self.amount = amount
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderPaymentRefund':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderPaymentRefund':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderPaymentRefund(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['OrderPayment_ID'] = self.order_payment_id
		if self.amount is not None:
			data['Amount'] = self.amount
		return data
