"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Option_Set_Default. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/option_set_default
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OptionSetDefault(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product_option: merchantapi.model.ProductOption = None):
		"""
		OptionSetDefault Constructor.

		:param client: Client
		:param product_option: ProductOption
		"""

		super().__init__(client)
		self.option_id = None
		self.option_code = None
		self.attribute_id = None
		self.option_default = None
		if isinstance(product_option, merchantapi.model.ProductOption):
			if product_option.get_id():
				self.set_option_id(product_option.get_id())
			elif product_option.get_code():
				self.set_option_code(product_option.get_code())

			if product_option.get_attribute_id():
				self.set_attribute_id(product_option.get_attribute_id())

			self.set_option_code(product_option.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Option_Set_Default'

	def get_option_id(self) -> int:
		"""
		Get Option_ID.

		:returns: int
		"""

		return self.option_id

	def get_option_code(self) -> str:
		"""
		Get Option_Code.

		:returns: str
		"""

		return self.option_code

	def get_attribute_id(self) -> int:
		"""
		Get Attribute_ID.

		:returns: int
		"""

		return self.attribute_id

	def get_option_default(self) -> bool:
		"""
		Get Option_Default.

		:returns: bool
		"""

		return self.option_default

	def set_option_id(self, option_id: int) -> 'OptionSetDefault':
		"""
		Set Option_ID.

		:param option_id: int
		:returns: OptionSetDefault
		"""

		self.option_id = option_id
		return self

	def set_option_code(self, option_code: str) -> 'OptionSetDefault':
		"""
		Set Option_Code.

		:param option_code: str
		:returns: OptionSetDefault
		"""

		self.option_code = option_code
		return self

	def set_attribute_id(self, attribute_id: int) -> 'OptionSetDefault':
		"""
		Set Attribute_ID.

		:param attribute_id: int
		:returns: OptionSetDefault
		"""

		self.attribute_id = attribute_id
		return self

	def set_option_default(self, option_default: bool) -> 'OptionSetDefault':
		"""
		Set Option_Default.

		:param option_default: bool
		:returns: OptionSetDefault
		"""

		self.option_default = option_default
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OptionSetDefault':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OptionSetDefault':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OptionSetDefault(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.option_id is not None:
			data['Option_ID'] = self.option_id
		elif self.option_code is not None:
			data['Option_Code'] = self.option_code

		if self.attribute_id is not None:
			data['Attribute_ID'] = self.attribute_id

		if self.option_code is not None:
			data['Option_Code'] = self.option_code
		if self.option_default is not None:
			data['Option_Default'] = self.option_default
		return data
