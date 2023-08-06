"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderListLoadQuery(ListQueryRequest):
	# PAY_STATUS_FILTER constants.
	PAY_STATUS_FILTER_AUTH_ONLY = 'auth_0_capt'
	PAY_STATUS_FILTER_PARTIAL_CAPTURE = 'partial_capt'
	PAY_STATUS_FILTER_CAPTURED_NOT_SHIPPED = 'capt_not_ship'
	PAY_STATUS_FILTER_SHIPPED_NOT_CAPTURED = 'ship_not_capt'

	available_search_fields = [
		'id',
		'batch_id',
		'status',
		'pay_status',
		'orderdate',
		'dt_instock',
		'ship_res',
		'ship_fname',
		'ship_lname',
		'ship_email',
		'ship_comp',
		'ship_phone',
		'ship_fax',
		'ship_addr1',
		'ship_addr2',
		'ship_city',
		'ship_state',
		'ship_zip',
		'ship_cntry',
		'bill_fname',
		'bill_lname',
		'bill_email',
		'bill_comp',
		'bill_phone',
		'bill_fax',
		'bill_addr1',
		'bill_addr2',
		'bill_city',
		'bill_state',
		'bill_zip',
		'bill_cntry',
		'ship_id',
		'ship_data',
		'source',
		'source_id',
		'total',
		'total_ship',
		'total_tax',
		'total_auth',
		'total_capt',
		'total_rfnd',
		'net_capt',
		'pend_count',
		'bord_count',
		'cust_login',
		'cust_pw_email',
		'business_title',
		'note_count'
	]

	available_sort_fields = [
		'id',
		'batch_id',
		'status',
		'pay_status',
		'orderdate',
		'dt_instock',
		'ship_res',
		'ship_fname',
		'ship_lname',
		'ship_email',
		'ship_comp',
		'ship_phone',
		'ship_fax',
		'ship_addr1',
		'ship_addr2',
		'ship_city',
		'ship_state',
		'ship_zip',
		'ship_cntry',
		'bill_fname',
		'bill_lname',
		'bill_email',
		'bill_comp',
		'bill_phone',
		'bill_fax',
		'bill_addr1',
		'bill_addr2',
		'bill_city',
		'bill_state',
		'bill_zip',
		'bill_cntry',
		'ship_data',
		'source',
		'source_id',
		'total',
		'total_ship',
		'total_tax',
		'total_auth',
		'total_capt',
		'total_rfnd',
		'net_capt',
		'pend_count',
		'bord_count',
		'cust_login',
		'cust_pw_email',
		'business_title',
		'note_count',
		'payment_module'
	]

	available_on_demand_columns = [
		'ship_method',
		'cust_login',
		'cust_pw_email',
		'business_title',
		'payment_module',
		'customer',
		'items',
		'charges',
		'coupons',
		'discounts',
		'payments',
		'notes',
		'parts',
		'shipments',
		'returns'
	]

	available_custom_filters = {
		'Customer_ID': 'int',
		'BusinessAccount_ID': 'int',
		'pay_id': 'int',
		'payment': [
			PAY_STATUS_FILTER_AUTH_ONLY,
			PAY_STATUS_FILTER_PARTIAL_CAPTURE,
			PAY_STATUS_FILTER_CAPTURED_NOT_SHIPPED,
			PAY_STATUS_FILTER_SHIPPED_NOT_CAPTURED
		],
		'product_code': 'string'
	}

	def __init__(self, client: Client = None):
		"""
		OrderListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.passphrase = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderList_Load_Query'

	def get_passphrase(self) -> str:
		"""
		Get Passphrase.

		:returns: str
		"""

		return self.passphrase

	def set_passphrase(self, passphrase: str) -> 'OrderListLoadQuery':
		"""
		Set Passphrase.

		:param passphrase: str
		:returns: OrderListLoadQuery
		"""

		self.passphrase = passphrase
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderListLoadQuery(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.passphrase is not None:
			data['Passphrase'] = self.passphrase
		return data
