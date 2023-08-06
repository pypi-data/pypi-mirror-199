"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for AttributeTemplateAttribute_Insert.

:see: https://docs.miva.com/json-api/functions/attributetemplateattribute_insert
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class AttributeTemplateAttributeInsert(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		AttributeTemplateAttributeInsert Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		self.data['data'] = merchantapi.model.AttributeTemplateAttribute(self.data['data'])

	def get_attribute_template_attribute(self) -> merchantapi.model.AttributeTemplateAttribute:
		"""
		Get attribute_template_attribute.

		:returns: AttributeTemplateAttribute
		"""

		return {} if 'data' not in self.data else self.data['data']
