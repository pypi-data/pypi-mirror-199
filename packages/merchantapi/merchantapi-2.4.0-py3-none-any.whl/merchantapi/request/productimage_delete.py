"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductImage_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productimage_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductImageDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_image_data: merchantapi.model.ProductImageData = None):
		"""
		ProductImageDelete Constructor.

		:param client: Client
		:param product_image_data: ProductImageData
		"""

		super().__init__(client)
		self.product_image_id = None
		if isinstance(product_image_data, merchantapi.model.ProductImageData):
			self.set_product_image_id(product_image_data.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductImage_Delete'

	def get_product_image_id(self) -> int:
		"""
		Get ProductImage_ID.

		:returns: int
		"""

		return self.product_image_id

	def set_product_image_id(self, product_image_id: int) -> 'ProductImageDelete':
		"""
		Set ProductImage_ID.

		:param product_image_id: int
		:returns: ProductImageDelete
		"""

		self.product_image_id = product_image_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductImageDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductImageDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductImageDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['ProductImage_ID'] = self.product_image_id
		return data
