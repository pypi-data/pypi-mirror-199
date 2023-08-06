"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductVariant_Generate_Delimiter. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariant_generate_delimiter
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.request import ProductVariantGenerate
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductVariantGenerateDelimiter(ProductVariantGenerate):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantGenerateDelimiter Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client, product)
		self.delimiter = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariant_Generate_Delimiter'

	def get_delimiter(self) -> str:
		"""
		Get Delimiter.

		:returns: str
		"""

		return self.delimiter

	def set_delimiter(self, delimiter: str) -> 'ProductVariantGenerateDelimiter':
		"""
		Set Delimiter.

		:param delimiter: str
		:returns: ProductVariantGenerateDelimiter
		"""

		self.delimiter = delimiter
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantGenerateDelimiter':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantGenerateDelimiter':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantGenerateDelimiter(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.delimiter is not None:
			data['Delimiter'] = self.delimiter
		return data
