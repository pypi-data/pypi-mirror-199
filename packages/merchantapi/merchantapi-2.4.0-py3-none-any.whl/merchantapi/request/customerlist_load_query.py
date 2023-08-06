"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CustomerList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/customerlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CustomerListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'login',
		'pw_email',
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
		'ship_res',
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
		'business_title',
		'note_count',
		'dt_created',
		'dt_login',
		'credit'
	]

	available_sort_fields = [
		'id',
		'login',
		'pw_email',
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
		'ship_res',
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
		'business_title',
		'note_count',
		'dt_created',
		'dt_login',
		'credit'
	]

	def __init__(self, client: Client = None):
		"""
		CustomerListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CustomerList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CustomerListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CustomerListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CustomerListLoadQuery(self, http_response, data)
