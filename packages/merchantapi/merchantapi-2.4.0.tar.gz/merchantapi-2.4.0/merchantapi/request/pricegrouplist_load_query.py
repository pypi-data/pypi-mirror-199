"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request PriceGroupList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/pricegrouplist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PriceGroupListLoadQuery(ListQueryRequest):

	available_search_fields = [
		'id',
		'name',
		'type',
		'module_id',
		'custscope',
		'rate',
		'discount',
		'markup',
		'dt_start',
		'dt_end',
		'priority',
		'exclusion',
		'descrip',
		'display',
		'qmn_subtot',
		'qmx_subtot',
		'qmn_quan',
		'qmx_quan',
		'qmn_weight',
		'qmx_weight',
		'bmn_subtot',
		'bmx_subtot',
		'bmn_quan',
		'bmx_quan',
		'bmn_weight',
		'bmx_weight'
	]

	available_sort_fields = [
		'id',
		'name',
		'type',
		'module_id',
		'custscope',
		'rate',
		'discount',
		'markup',
		'dt_start',
		'dt_end',
		'priority',
		'exclusion',
		'descrip',
		'display',
		'qmn_subtot',
		'qmx_subtot',
		'qmn_quan',
		'qmx_quan',
		'qmn_weight',
		'qmx_weight',
		'bmn_subtot',
		'bmx_subtot',
		'bmn_quan',
		'bmx_quan',
		'bmn_weight',
		'bmx_weight'
	]

	def __init__(self, client: Client = None):
		"""
		PriceGroupListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'PriceGroupList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PriceGroupListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PriceGroupListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PriceGroupListLoadQuery(self, http_response, data)
