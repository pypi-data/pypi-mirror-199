"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request SubscriptionList_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/subscriptionlist_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class SubscriptionListDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		SubscriptionListDelete Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.subscription_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'SubscriptionList_Delete'

	def get_subscription_ids(self):
		"""
		Get Subscription_IDs.

		:returns: list
		"""

		return self.subscription_ids
	
	def add_subscription_id(self, subscription_id) -> 'SubscriptionListDelete':
		"""
		Add Subscription_IDs.

		:param subscription_id: int
		:returns: {SubscriptionListDelete}
		"""

		self.subscription_ids.append(subscription_id)
		return self

	def add_subscription(self, subscription: merchantapi.model.Subscription) -> 'SubscriptionListDelete':
		"""
		Add Subscription model.

		:param subscription: Subscription
		:raises Exception:
		:returns: SubscriptionListDelete
		"""
		if not isinstance(subscription, merchantapi.model.Subscription):
			raise Exception('Expected an instance of Subscription')

		if subscription.get_id():
			self.subscription_ids.append(subscription.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.SubscriptionListDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'SubscriptionListDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.SubscriptionListDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Subscription_IDs'] = self.subscription_ids
		return data
