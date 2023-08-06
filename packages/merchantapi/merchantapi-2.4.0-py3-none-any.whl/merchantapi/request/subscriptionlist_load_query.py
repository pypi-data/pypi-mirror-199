"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request SubscriptionList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/subscriptionlist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class SubscriptionListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'order_id',
		'quantity',
		'termrem',
		'termproc',
		'firstdate',
		'lastdate',
		'nextdate',
		'status',
		'message',
		'cncldate',
		'tax',
		'shipping',
		'subtotal',
		'total',
		'authfails',
		'lastafail',
		'frequency',
		'term',
		'descrip',
		'n',
		'fixed_dow',
		'fixed_dom',
		'sub_count',
		'customer_login',
		'customer_pw_email',
		'customer_business_title',
		'product_code',
		'product_name',
		'product_sku',
		'product_price',
		'product_cost',
		'product_weight',
		'product_descrip',
		'product_taxable',
		'product_thumbnail',
		'product_image',
		'product_active',
		'product_page_title',
		'product_cancat_code',
		'product_page_code',
		'address_descrip',
		'address_fname',
		'address_lname',
		'address_email',
		'address_phone',
		'address_fax',
		'address_comp',
		'address_addr1',
		'address_addr2',
		'address_city',
		'address_state',
		'address_zip',
		'address_cntry',
		'product_inventory_active'
	]

	available_sort_fields = [
		'id',
		'order_id',
		'custpc_id',
		'quantity',
		'termrem',
		'termproc',
		'firstdate',
		'lastdate',
		'nextdate',
		'status',
		'message',
		'cncldate',
		'tax',
		'shipping',
		'subtotal',
		'total',
		'authfails',
		'lastafail',
		'frequency',
		'term',
		'descrip',
		'n',
		'fixed_dow',
		'fixed_dom',
		'sub_count',
		'customer_login',
		'customer_pw_email',
		'customer_business_title',
		'product_code',
		'product_name',
		'product_sku',
		'product_cancat_code',
		'product_page_code',
		'product_price',
		'product_cost',
		'product_weight',
		'product_descrip',
		'product_taxable',
		'product_thumbnail',
		'product_image',
		'product_active',
		'product_page_title',
		'address_descrip',
		'address_fname',
		'address_lname',
		'address_email',
		'address_phone',
		'address_fax',
		'address_comp',
		'address_addr1',
		'address_addr2',
		'address_city',
		'address_state',
		'address_zip',
		'address_cntry',
		'product_inventory'
	]

	available_on_demand_columns = [
		'imagetypes',
		'imagetype_count',
		'product_descrip'
	]

	def __init__(self, client: Client = None):
		"""
		SubscriptionListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'SubscriptionList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.SubscriptionListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'SubscriptionListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.SubscriptionListLoadQuery(self, http_response, data)
