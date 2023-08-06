"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for PriceGroupExcludedProduct_Update_Assigned.

:see: https://docs.miva.com/json-api/functions/pricegroupexcludedproduct_update_assigned
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class PriceGroupExcludedProductUpdateAssigned(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		PriceGroupExcludedProductUpdateAssigned Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data and isinstance(self.data['data'], list):
			for i, e in enumerate(self.data['data'], 0):
				self.data['data'][i] = merchantapi.model.PriceGroupProduct(e)

	def get_price_group_products(self):
		"""
		Get price_group_products.

		:returns: list of PriceGroupProduct
		"""

		return self.data['data'] if self.data['data'] is not None else []
