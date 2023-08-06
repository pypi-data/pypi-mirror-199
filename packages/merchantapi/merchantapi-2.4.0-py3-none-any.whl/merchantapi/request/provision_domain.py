"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Provision_Domain. 
Scope: Domain.
:see: https://docs.miva.com/json-api/functions/provision_domain
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProvisionDomain(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		ProvisionDomain Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.scope = merchantapi.abstract.Request.SCOPE_DOMAIN
		self.xml = None

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Provision_Domain'

	def get_xml(self) -> str:
		"""
		Get xml.

		:returns: str
		"""

		return self.xml

	def set_xml(self, xml: str) -> 'ProvisionDomain':
		"""
		Set xml.

		:param xml: str
		:returns: ProvisionDomain
		"""

		self.xml = xml
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProvisionDomain':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProvisionDomain':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProvisionDomain(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['XML'] = self.xml
		return data
