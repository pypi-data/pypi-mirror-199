"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for AttributeTemplateOption_Insert.

:see: https://docs.miva.com/json-api/functions/attributetemplateoption_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class AttributeTemplateOptionInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateOptionInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.AttributeTemplateOption(self.data['data'])

	def get_attribute_template_option(self) -> merchantapi.model.AttributeTemplateOption:
		"""
		Get attribute_template_option.

		:returns: AttributeTemplateOption
		"""

		return {} if 'data' not in self.data else self.data['data']
