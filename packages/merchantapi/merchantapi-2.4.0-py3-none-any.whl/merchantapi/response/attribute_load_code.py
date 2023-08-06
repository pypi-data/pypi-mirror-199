"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for Attribute_Load_Code.

:see: https://docs.miva.com/json-api/functions/attribute_load_code
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class AttributeLoadCode(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeLoadCode Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.ProductAttribute(self.data['data'])

	def get_product_attribute(self) -> merchantapi.model.ProductAttribute:
		"""
		Get product_attribute.

		:returns: ProductAttribute
		"""

		return {} if 'data' not in self.data else self.data['data']
