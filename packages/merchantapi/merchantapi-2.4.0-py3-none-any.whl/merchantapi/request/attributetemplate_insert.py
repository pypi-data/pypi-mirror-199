"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request AttributeTemplate_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/attributetemplate_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class AttributeTemplateInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		AttributeTemplateInsert Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.code = None
		self.prompt = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'AttributeTemplate_Insert'

	def get_code(self) -> str:
		"""
		Get Code.

		:returns: str
		"""

		return self.code

	def get_prompt(self) -> str:
		"""
		Get Prompt.

		:returns: str
		"""

		return self.prompt

	def set_code(self, code: str) -> 'AttributeTemplateInsert':
		"""
		Set Code.

		:param code: str
		:returns: AttributeTemplateInsert
		"""

		self.code = code
		return self

	def set_prompt(self, prompt: str) -> 'AttributeTemplateInsert':
		"""
		Set Prompt.

		:param prompt: str
		:returns: AttributeTemplateInsert
		"""

		self.prompt = prompt
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.AttributeTemplateInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'AttributeTemplateInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.AttributeTemplateInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Code'] = self.code
		data['Prompt'] = self.prompt
		return data
