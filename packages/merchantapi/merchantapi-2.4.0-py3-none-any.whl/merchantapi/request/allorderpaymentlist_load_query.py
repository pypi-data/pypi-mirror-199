"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AllOrderPaymentList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/allorderpaymentlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import OrderListLoadQuery
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AllOrderPaymentListLoadQuery(OrderListLoadQuery):

	available_search_fields = [
		'type',
		'refnum',
		'available',
		'expires,',
		'payment_ip',
		'amount',
		'payment_dtstamp',
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

	available_sort_fields = [
		'type',
		'refnum',
		'available',
		'expires,',
		'payment_ip',
		'amount',
		'payment_dtstamp'
	]

	def __init__(self, client: Client = None):
		"""
		AllOrderPaymentListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AllOrderPaymentList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AllOrderPaymentListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AllOrderPaymentListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AllOrderPaymentListLoadQuery(self, http_response, data)
