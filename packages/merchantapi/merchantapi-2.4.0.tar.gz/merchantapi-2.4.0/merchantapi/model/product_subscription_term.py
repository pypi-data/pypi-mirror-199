"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductSubscriptionTerm data model.
"""

from merchantapi.abstract import Model
from .product_subscription_term_date import ProductSubscriptionTermDate

class ProductSubscriptionTerm(Model):
	# TERM_FREQUENCY constants.
	TERM_FREQUENCY_N_DAYS = 'n'
	TERM_FREQUENCY_N_MONTHS = 'n_months'
	TERM_FREQUENCY_DAILY = 'daily'
	TERM_FREQUENCY_WEEKLY = 'weekly'
	TERM_FREQUENCY_BIWEEKLY = 'biweekly'
	TERM_FREQUENCY_QUARTERLY = 'quarterly'
	TERM_FREQUENCY_SEMIANNUALLY = 'semiannually'
	TERM_FREQUENCY_ANNUALLY = 'annually'
	TERM_FREQUENCY_FIXED_WEEKLY = 'fixedweekly'
	TERM_FREQUENCY_FIXED_MONTHLY = 'fixedmonthly'
	TERM_FREQUENCY_DATES = 'dates'
	TERM_FREQUENCY_MONTHLY = 'monthly'

	def __init__(self, data: dict = None):
		"""
		ProductSubscriptionTerm Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('dates'):
			value = self.get_field('dates')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductSubscriptionTermDate):
							value[i] = ProductSubscriptionTermDate(e)
					else:
						raise Exception('Expected list of ProductSubscriptionTermDate or dict')
			else:
				raise Exception('Expected list of ProductSubscriptionTermDate or dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_frequency(self) -> str:
		"""
		Get frequency.

		:returns: string
		"""

		return self.get_field('frequency')

	def get_term(self) -> int:
		"""
		Get term.

		:returns: int
		"""

		return self.get_field('term', 0)

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_n(self) -> int:
		"""
		Get n.

		:returns: int
		"""

		return self.get_field('n', 0)

	def get_fixed_day_of_week(self) -> int:
		"""
		Get fixed_dow.

		:returns: int
		"""

		return self.get_field('fixed_dow', 0)

	def get_fixed_day_of_month(self) -> int:
		"""
		Get fixed_dom.

		:returns: int
		"""

		return self.get_field('fixed_dom', 0)

	def get_subscription_count(self) -> int:
		"""
		Get sub_count.

		:returns: int
		"""

		return self.get_field('sub_count', 0)

	def get_dates(self):
		"""
		Get dates.

		:returns: List of ProductSubscriptionTermDate
		"""

		return self.get_field('dates', [])

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'dates' in ret and isinstance(ret['dates'], list):
			for i, e in enumerate(ret['dates']):
				if isinstance(e, ProductSubscriptionTermDate):
					ret['dates'][i] = ret['dates'][i].to_dict()

		return ret
