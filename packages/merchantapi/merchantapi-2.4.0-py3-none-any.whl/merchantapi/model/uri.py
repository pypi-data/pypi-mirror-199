"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Uri data model.
"""

from merchantapi.abstract import Model
from .uri_detail import UriDetail

class Uri(Model):
	# DESTINATION_TYPE constants.
	DESTINATION_TYPE_SCREEN = 'screen'
	DESTINATION_TYPE_PAGE = 'page'
	DESTINATION_TYPE_CATEGORY = 'category'
	DESTINATION_TYPE_PRODUCT = 'product'
	DESTINATION_TYPE_FEED = 'feed'

	def __init__(self, data: dict = None):
		"""
		Uri Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('store'):
			value = self.get_field('store')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('store', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('product'):
			value = self.get_field('product')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('product', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('category'):
			value = self.get_field('category')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('category', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('page'):
			value = self.get_field('page')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('page', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

		if self.has_field('feed'):
			value = self.get_field('feed')
			if isinstance(value, dict):
				if not isinstance(value, UriDetail):
					self.set_field('feed', UriDetail(value))
			else:
				raise Exception('Expected UriDetail or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_uri(self) -> str:
		"""
		Get uri.

		:returns: string
		"""

		return self.get_field('uri')

	def get_store_id(self) -> int:
		"""
		Get store_id.

		:returns: int
		"""

		return self.get_field('store_id', 0)

	def get_screen(self) -> str:
		"""
		Get screen.

		:returns: string
		"""

		return self.get_field('screen')

	def get_page_id(self) -> int:
		"""
		Get page_id.

		:returns: int
		"""

		return self.get_field('page_id', 0)

	def get_category_id(self) -> int:
		"""
		Get cat_id.

		:returns: int
		"""

		return self.get_field('cat_id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_feed_id(self) -> int:
		"""
		Get feed_id.

		:returns: int
		"""

		return self.get_field('feed_id', 0)

	def get_canonical(self) -> bool:
		"""
		Get canonical.

		:returns: bool
		"""

		return self.get_field('canonical', False)

	def get_status(self) -> int:
		"""
		Get status.

		:returns: int
		"""

		return self.get_field('status', 0)

	def get_store(self):
		"""
		Get store.

		:returns: UriDetail|None
		"""

		return self.get_field('store', None)

	def get_product(self):
		"""
		Get product.

		:returns: UriDetail|None
		"""

		return self.get_field('product', None)

	def get_category(self):
		"""
		Get category.

		:returns: UriDetail|None
		"""

		return self.get_field('category', None)

	def get_page(self):
		"""
		Get page.

		:returns: UriDetail|None
		"""

		return self.get_field('page', None)

	def get_feed(self):
		"""
		Get feed.

		:returns: UriDetail|None
		"""

		return self.get_field('feed', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'store' in ret and isinstance(ret['store'], UriDetail):
			ret['store'] = ret['store'].to_dict()

		if 'product' in ret and isinstance(ret['product'], UriDetail):
			ret['product'] = ret['product'].to_dict()

		if 'category' in ret and isinstance(ret['category'], UriDetail):
			ret['category'] = ret['category'].to_dict()

		if 'page' in ret and isinstance(ret['page'], UriDetail):
			ret['page'] = ret['page'].to_dict()

		if 'feed' in ret and isinstance(ret['feed'], UriDetail):
			ret['feed'] = ret['feed'].to_dict()

		return ret
