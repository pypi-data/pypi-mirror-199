"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for Option_Load_Code.

:see: https://docs.miva.com/json-api/functions/option_load_code
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class OptionLoadCode(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		OptionLoadCode Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.ProductOption(self.data['data'])

	def get_product_option(self) -> merchantapi.model.ProductOption:
		"""
		Get product_option.

		:returns: ProductOption
		"""

		return {} if 'data' not in self.data else self.data['data']
