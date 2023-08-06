"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Module. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/module
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class Module(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		Module Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.module_code = None
		self.module_function = None
		self.module_fields = {}

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Module'

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: str
		"""

		return self.module_code

	def get_module_function(self) -> str:
		"""
		Get Module_Function.

		:returns: str
		"""

		return self.module_function

	def get_module_fields(self):
		"""
		Get Module_Fields.

		:returns: dict
		"""

		return self.module_fields

	def set_module_code(self, module_code: str) -> 'Module':
		"""
		Set Module_Code.

		:param module_code: str
		:returns: Module
		"""

		self.module_code = module_code
		return self

	def set_module_function(self, module_function: str) -> 'Module':
		"""
		Set Module_Function.

		:param module_function: str
		:returns: Module
		"""

		self.module_function = module_function
		return self

	def set_module_fields(self, module_fields) -> 'Module':
		"""
		Set Module_Fields.

		:param module_fields: dict
		:returns: Module
		"""

		self.module_fields = module_fields
		return self

	def set_module_field(self, field: str, value) -> 'Module':
		"""
		Add custom data to the request.

		:param field: str
		:param value: mixed
		:returns: {Module}
		"""

		self.module_fields[field] = value
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.Module':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'Module':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.Module(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()
		data.update(self.get_module_fields())

		data['Module_Code'] = self.module_code
		data['Module_Function'] = self.module_function
		return data
