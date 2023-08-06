"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for ProductImage_Add.

:see: https://docs.miva.com/json-api/functions/productimage_add
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class ProductImageAdd(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductImageAdd Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.ProductImageData(self.data['data'])

	def get_product_image_data(self) -> merchantapi.model.ProductImageData:
		"""
		Get product_image_data.

		:returns: ProductImageData
		"""

		return {} if 'data' not in self.data else self.data['data']
