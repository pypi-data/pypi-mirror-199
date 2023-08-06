"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductImage_Update_Type. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productimage_update_type
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductImageUpdateType(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProductImageUpdateType Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.product_image_id = None
		self.image_type_id = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductImage_Update_Type'

	def get_product_image_id(self) -> int:
		"""
		Get ProductImage_ID.

		:returns: int
		"""

		return self.product_image_id

	def get_image_type_id(self) -> int:
		"""
		Get ImageType_ID.

		:returns: int
		"""

		return self.image_type_id

	def set_product_image_id(self, product_image_id: int) -> 'ProductImageUpdateType':
		"""
		Set ProductImage_ID.

		:param product_image_id: int
		:returns: ProductImageUpdateType
		"""

		self.product_image_id = product_image_id
		return self

	def set_image_type_id(self, image_type_id: int) -> 'ProductImageUpdateType':
		"""
		Set ImageType_ID.

		:param image_type_id: int
		:returns: ProductImageUpdateType
		"""

		self.image_type_id = image_type_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductImageUpdateType':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductImageUpdateType':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductImageUpdateType(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['ProductImage_ID'] = self.product_image_id
		if self.image_type_id is not None:
			data['ImageType_ID'] = self.image_type_id
		return data
