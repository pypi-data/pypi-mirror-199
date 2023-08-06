"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for ProductVariant_Generate_Delimiter.

:see: https://docs.miva.com/json-api/functions/productvariant_generate_delimiter
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model
from .productvariant_generate import ProductVariantGenerate

class ProductVariantGenerateDelimiter(ProductVariantGenerate):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		ProductVariantGenerateDelimiter Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
