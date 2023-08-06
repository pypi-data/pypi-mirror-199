"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Order data model.
"""

from merchantapi.abstract import Model
from .customer import Customer
from .order_item import OrderItem
from .order_charge import OrderCharge
from .order_coupon import OrderCoupon
from .order_discount_total import OrderDiscountTotal
from .order_payment import OrderPayment
from .order_note import OrderNote
from .order_part import OrderPart
from .custom_field_values import CustomFieldValues
from .order_shipment import OrderShipment
from .order_return import OrderReturn

class Order(Model):
	# ORDER_STATUS constants.
	ORDER_STATUS_PENDING = 0
	ORDER_STATUS_PROCESSING = 100
	ORDER_STATUS_SHIPPED = 200
	ORDER_STATUS_PARTIALLY_SHIPPED = 201
	ORDER_STATUS_CANCELLED = 300
	ORDER_STATUS_BACKORDERED = 400
	ORDER_STATUS_RMA_ISSUED = 500
	ORDER_STATUS_RETURNED = 600

	# ORDER_PAYMENT_STATUS constants.
	ORDER_PAYMENT_STATUS_PENDING = 0
	ORDER_PAYMENT_STATUS_AUTHORIZED = 100
	ORDER_PAYMENT_STATUS_CAPTURED = 200
	ORDER_PAYMENT_STATUS_PARTIALLY_CAPTURED = 201

	# ORDER_STOCK_STATUS constants.
	ORDER_STOCK_STATUS_AVAILABLE = 100
	ORDER_STOCK_STATUS_UNAVAILABLE = 200
	ORDER_STOCK_STATUS_PARTIAL = 201

	def __init__(self, data: dict = None):
		"""
		Order Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('customer'):
			value = self.get_field('customer')
			if isinstance(value, dict):
				if not isinstance(value, Customer):
					self.set_field('customer', Customer(value))
			else:
				raise Exception('Expected Customer or a dict')

		if self.has_field('items'):
			value = self.get_field('items')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderItem):
							value[i] = OrderItem(e)
					else:
						raise Exception('Expected list of OrderItem or dict')
			else:
				raise Exception('Expected list of OrderItem or dict')

		if self.has_field('charges'):
			value = self.get_field('charges')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderCharge):
							value[i] = OrderCharge(e)
					else:
						raise Exception('Expected list of OrderCharge or dict')
			else:
				raise Exception('Expected list of OrderCharge or dict')

		if self.has_field('coupons'):
			value = self.get_field('coupons')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderCoupon):
							value[i] = OrderCoupon(e)
					else:
						raise Exception('Expected list of OrderCoupon or dict')
			else:
				raise Exception('Expected list of OrderCoupon or dict')

		if self.has_field('discounts'):
			value = self.get_field('discounts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderDiscountTotal):
							value[i] = OrderDiscountTotal(e)
					else:
						raise Exception('Expected list of OrderDiscountTotal or dict')
			else:
				raise Exception('Expected list of OrderDiscountTotal or dict')

		if self.has_field('payments'):
			value = self.get_field('payments')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderPayment):
							value[i] = OrderPayment(e)
					else:
						raise Exception('Expected list of OrderPayment or dict')
			else:
				raise Exception('Expected list of OrderPayment or dict')

		if self.has_field('notes'):
			value = self.get_field('notes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderNote):
							value[i] = OrderNote(e)
					else:
						raise Exception('Expected list of OrderNote or dict')
			else:
				raise Exception('Expected list of OrderNote or dict')

		if self.has_field('parts'):
			value = self.get_field('parts')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderPart):
							value[i] = OrderPart(e)
					else:
						raise Exception('Expected list of OrderPart or dict')
			else:
				raise Exception('Expected list of OrderPart or dict')

		if self.has_field('CustomField_Values'):
			value = self.get_field('CustomField_Values')
			if isinstance(value, dict):
				if not isinstance(value, CustomFieldValues):
					self.set_field('CustomField_Values', CustomFieldValues(value))
			else:
				raise Exception('Expected CustomFieldValues or a dict')

		if self.has_field('shipments'):
			value = self.get_field('shipments')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderShipment):
							value[i] = OrderShipment(e)
					else:
						raise Exception('Expected list of OrderShipment or dict')
			else:
				raise Exception('Expected list of OrderShipment or dict')

		if self.has_field('returns'):
			value = self.get_field('returns')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, OrderReturn):
							value[i] = OrderReturn(e)
					else:
						raise Exception('Expected list of OrderReturn or dict')
			else:
				raise Exception('Expected list of OrderReturn or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_payment_id(self) -> int:
		"""
		Get pay_id.

		:returns: int
		"""

		return self.get_field('pay_id', 0)

	def get_batch_id(self) -> int:
		"""
		Get batch_id.

		:returns: int
		"""

		return self.get_field('batch_id', 0)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_payment_status(self) -> int:
		"""
		Get pay_status.

		:returns: int
		"""

		return self.get_field('pay_status', 0)

	def get_stock_status(self) -> int:
		"""
		Get stk_status.

		:returns: int
		"""

		return self.get_field('stk_status', 0)

	def get_date_in_stock(self) -> int:
		"""
		Get dt_instock.

		:returns: int
		"""

		return self.get_timestamp_field('dt_instock')

	def get_order_date(self) -> int:
		"""
		Get orderdate.

		:returns: int
		"""

		return self.get_field('orderdate', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_ship_residential(self) -> bool:
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

	def get_shipment_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_ship_data(self) -> str:
		"""
		Get ship_data.

		:returns: string
		"""

		return self.get_field('ship_data')

	def get_ship_method(self) -> str:
		"""
		Get ship_method.

		:returns: string
		"""

		return self.get_field('ship_method')

	def get_customer_login(self) -> str:
		"""
		Get cust_login.

		:returns: string
		"""

		return self.get_field('cust_login')

	def get_customer_password_email(self) -> str:
		"""
		Get cust_pw_email.

		:returns: string
		"""

		return self.get_field('cust_pw_email')

	def get_business_title(self) -> str:
		"""
		Get business_title.

		:returns: string
		"""

		return self.get_field('business_title')

	def get_payment_module(self) -> str:
		"""
		Get payment_module.

		:returns: string
		"""

		return self.get_field('payment_module')

	def get_source(self) -> str:
		"""
		Get source.

		:returns: string
		"""

		return self.get_field('source')

	def get_source_id(self) -> int:
		"""
		Get source_id.

		:returns: int
		"""

		return self.get_field('source_id', 0)

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_formatted_total(self) -> str:
		"""
		Get formatted_total.

		:returns: string
		"""

		return self.get_field('formatted_total')

	def get_total_ship(self) -> float:
		"""
		Get total_ship.

		:returns: float
		"""

		return self.get_field('total_ship', 0.00)

	def get_formatted_total_ship(self) -> str:
		"""
		Get formatted_total_ship.

		:returns: string
		"""

		return self.get_field('formatted_total_ship')

	def get_total_tax(self) -> float:
		"""
		Get total_tax.

		:returns: float
		"""

		return self.get_field('total_tax', 0.00)

	def get_formatted_total_tax(self) -> str:
		"""
		Get formatted_total_tax.

		:returns: string
		"""

		return self.get_field('formatted_total_tax')

	def get_total_authorized(self) -> float:
		"""
		Get total_auth.

		:returns: float
		"""

		return self.get_field('total_auth', 0.00)

	def get_formatted_total_authorized(self) -> str:
		"""
		Get formatted_total_auth.

		:returns: string
		"""

		return self.get_field('formatted_total_auth')

	def get_total_captured(self) -> float:
		"""
		Get total_capt.

		:returns: float
		"""

		return self.get_field('total_capt', 0.00)

	def get_formatted_total_captured(self) -> str:
		"""
		Get formatted_total_capt.

		:returns: string
		"""

		return self.get_field('formatted_total_capt')

	def get_total_refunded(self) -> float:
		"""
		Get total_rfnd.

		:returns: float
		"""

		return self.get_field('total_rfnd', 0.00)

	def get_formatted_total_refunded(self) -> str:
		"""
		Get formatted_total_rfnd.

		:returns: string
		"""

		return self.get_field('formatted_total_rfnd')

	def get_net_captured(self) -> float:
		"""
		Get net_capt.

		:returns: float
		"""

		return self.get_field('net_capt', 0.00)

	def get_formatted_net_captured(self) -> str:
		"""
		Get formatted_net_capt.

		:returns: string
		"""

		return self.get_field('formatted_net_capt')

	def get_pending_count(self) -> int:
		"""
		Get pend_count.

		:returns: int
		"""

		return self.get_field('pend_count', 0)

	def get_backorder_count(self) -> int:
		"""
		Get bord_count.

		:returns: int
		"""

		return self.get_field('bord_count', 0)

	def get_note_count(self) -> int:
		"""
		Get note_count.

		:returns: int
		"""

		return self.get_field('note_count', 0)

	def get_customer(self):
		"""
		Get customer.

		:returns: Customer|None
		"""

		return self.get_field('customer', None)

	def get_items(self):
		"""
		Get items.

		:returns: List of OrderItem
		"""

		return self.get_field('items', [])

	def get_charges(self):
		"""
		Get charges.

		:returns: List of OrderCharge
		"""

		return self.get_field('charges', [])

	def get_coupons(self):
		"""
		Get coupons.

		:returns: List of OrderCoupon
		"""

		return self.get_field('coupons', [])

	def get_discounts(self):
		"""
		Get discounts.

		:returns: List of OrderDiscountTotal
		"""

		return self.get_field('discounts', [])

	def get_payments(self):
		"""
		Get payments.

		:returns: List of OrderPayment
		"""

		return self.get_field('payments', [])

	def get_notes(self):
		"""
		Get notes.

		:returns: List of OrderNote
		"""

		return self.get_field('notes', [])

	def get_parts(self):
		"""
		Get parts.

		:returns: List of OrderPart
		"""

		return self.get_field('parts', [])

	def get_custom_field_values(self):
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues|None
		"""

		return self.get_field('CustomField_Values', None)

	def get_dt_updated(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_timestamp_field('dt_updated')

	def get_shipments(self):
		"""
		Get shipments.

		:returns: List of OrderShipment
		"""

		return self.get_field('shipments', [])

	def get_returns(self):
		"""
		Get returns.

		:returns: List of OrderReturn
		"""

		return self.get_field('returns', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'customer' in ret and isinstance(ret['customer'], Customer):
			ret['customer'] = ret['customer'].to_dict()

		if 'items' in ret and isinstance(ret['items'], list):
			for i, e in enumerate(ret['items']):
				if isinstance(e, OrderItem):
					ret['items'][i] = ret['items'][i].to_dict()

		if 'charges' in ret and isinstance(ret['charges'], list):
			for i, e in enumerate(ret['charges']):
				if isinstance(e, OrderCharge):
					ret['charges'][i] = ret['charges'][i].to_dict()

		if 'coupons' in ret and isinstance(ret['coupons'], list):
			for i, e in enumerate(ret['coupons']):
				if isinstance(e, OrderCoupon):
					ret['coupons'][i] = ret['coupons'][i].to_dict()

		if 'discounts' in ret and isinstance(ret['discounts'], list):
			for i, e in enumerate(ret['discounts']):
				if isinstance(e, OrderDiscountTotal):
					ret['discounts'][i] = ret['discounts'][i].to_dict()

		if 'payments' in ret and isinstance(ret['payments'], list):
			for i, e in enumerate(ret['payments']):
				if isinstance(e, OrderPayment):
					ret['payments'][i] = ret['payments'][i].to_dict()

		if 'notes' in ret and isinstance(ret['notes'], list):
			for i, e in enumerate(ret['notes']):
				if isinstance(e, OrderNote):
					ret['notes'][i] = ret['notes'][i].to_dict()

		if 'parts' in ret and isinstance(ret['parts'], list):
			for i, e in enumerate(ret['parts']):
				if isinstance(e, OrderPart):
					ret['parts'][i] = ret['parts'][i].to_dict()

		if 'CustomField_Values' in ret and isinstance(ret['CustomField_Values'], CustomFieldValues):
			ret['CustomField_Values'] = ret['CustomField_Values'].to_dict()

		if 'shipments' in ret and isinstance(ret['shipments'], list):
			for i, e in enumerate(ret['shipments']):
				if isinstance(e, OrderShipment):
					ret['shipments'][i] = ret['shipments'][i].to_dict()

		if 'returns' in ret and isinstance(ret['returns'], list):
			for i, e in enumerate(ret['returns']):
				if isinstance(e, OrderReturn):
					ret['returns'][i] = ret['returns'][i].to_dict()

		return ret
