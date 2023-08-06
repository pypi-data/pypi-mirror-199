"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

RelatedProduct data model.
"""

from merchantapi.abstract import Model

class RelatedProduct(Model):
	def __init__(self, data: dict = None):
		"""
		RelatedProduct Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_thumbnail(self) -> str:
		"""
		Get thumbnail.

		:returns: string
		"""

		return self.get_field('thumbnail')

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_price(self) -> float:
		"""
		Get price.

		:returns: float
		"""

		return self.get_field('price', 0.00)

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_cost(self) -> float:
		"""
		Get cost.

		:returns: float
		"""

		return self.get_field('cost', 0.00)

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_weight(self) -> float:
		"""
		Get weight.

		:returns: float
		"""

		return self.get_field('weight', 0.00)

	def get_active(self) -> bool:
		"""
		Get active.

		:returns: bool
		"""

		return self.get_field('active', False)

	def get_page_title(self) -> str:
		"""
		Get page_title.

		:returns: string
		"""

		return self.get_field('page_title')

	def get_taxable(self) -> bool:
		"""
		Get taxable.

		:returns: bool
		"""

		return self.get_field('taxable', False)

	def get_date_time_created(self) -> int:
		"""
		Get dt_created.

		:returns: int
		"""

		return self.get_timestamp_field('dt_created')

	def get_date_time_updated(self) -> int:
		"""
		Get dt_updated.

		:returns: int
		"""

		return self.get_timestamp_field('dt_updated')

	def get_assigned(self) -> bool:
		"""
		Get assigned.

		:returns: bool
		"""

		return self.get_field('assigned', False)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		return self.get_field('disp_order', 0)
