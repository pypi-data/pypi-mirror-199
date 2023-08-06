"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CategoryList_Load_Query. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/categorylist_load_query
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.listquery import ListQueryRequest
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CategoryListLoadQuery(ListQueryRequest):
	# CATEGORY_SHOW constants.
	CATEGORY_SHOW_ALL = 'All'
	CATEGORY_SHOW_ACTIVE = 'Active'

	available_search_fields = [
		'id',
		'code',
		'name',
		'page_title',
		'parent_category',
		'page_code',
		'dt_created',
		'dt_updated',
		'depth'
	]

	available_sort_fields = [
		'id',
		'code',
		'name',
		'page_title',
		'active',
		'page_code',
		'parent_category',
		'disp_order',
		'dt_created',
		'dt_updated',
		'depth'
	]

	available_on_demand_columns = [
		'uris'
	]

	available_custom_filters = {
		'Category_Show': [
			CATEGORY_SHOW_ALL,
			CATEGORY_SHOW_ACTIVE
		]
	}

	def __init__(self, client: Client = None):
		"""
		CategoryListLoadQuery Constructor.

		:param client: Client
		"""

		super().__init__(client)

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CategoryList_Load_Query'

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CategoryListLoadQuery':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CategoryListLoadQuery':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CategoryListLoadQuery(self, http_response, data)
