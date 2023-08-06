"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Product_Insert. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/product_insert
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductInsert(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductInsert Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_code = None
		self.product_sku = None
		self.product_name = None
		self.product_description = None
		self.product_canonical_category_code = None
		self.product_alternate_display_page = None
		self.product_page_title = None
		self.product_thumbnail = None
		self.product_image = None
		self.product_price = None
		self.product_cost = None
		self.product_weight = None
		self.product_inventory = None
		self.product_taxable = None
		self.product_active = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(product, merchantapi.model.Product):
			self.set_product_code(product.get_code())
			self.set_product_sku(product.get_sku())
			self.set_product_name(product.get_name())
			self.set_product_description(product.get_description())
			self.set_product_canonical_category_code(product.get_canonical_category_code())
			self.set_product_alternate_display_page(product.get_page_code())
			self.set_product_page_title(product.get_page_title())
			self.set_product_thumbnail(product.get_thumbnail())
			self.set_product_image(product.get_image())
			self.set_product_price(product.get_price())
			self.set_product_cost(product.get_cost())
			self.set_product_weight(product.get_weight())
			self.set_product_inventory(product.get_product_inventory())
			self.set_product_taxable(product.get_taxable())
			self.set_product_active(product.get_active())

			if product.get_custom_field_values():
				self.set_custom_field_values(product.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Product_Insert'

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_product_name(self) -> str:
		"""
		Get Product_Name.

		:returns: str
		"""

		return self.product_name

	def get_product_description(self) -> str:
		"""
		Get Product_Description.

		:returns: str
		"""

		return self.product_description

	def get_product_canonical_category_code(self) -> str:
		"""
		Get Product_Canonical_Category_Code.

		:returns: str
		"""

		return self.product_canonical_category_code

	def get_product_alternate_display_page(self) -> str:
		"""
		Get Product_Alternate_Display_Page.

		:returns: str
		"""

		return self.product_alternate_display_page

	def get_product_page_title(self) -> str:
		"""
		Get Product_Page_Title.

		:returns: str
		"""

		return self.product_page_title

	def get_product_thumbnail(self) -> str:
		"""
		Get Product_Thumbnail.

		:returns: str
		"""

		return self.product_thumbnail

	def get_product_image(self) -> str:
		"""
		Get Product_Image.

		:returns: str
		"""

		return self.product_image

	def get_product_price(self) -> float:
		"""
		Get Product_Price.

		:returns: float
		"""

		return self.product_price

	def get_product_cost(self) -> float:
		"""
		Get Product_Cost.

		:returns: float
		"""

		return self.product_cost

	def get_product_weight(self) -> float:
		"""
		Get Product_Weight.

		:returns: float
		"""

		return self.product_weight

	def get_product_inventory(self) -> int:
		"""
		Get Product_Inventory.

		:returns: int
		"""

		return self.product_inventory

	def get_product_taxable(self) -> bool:
		"""
		Get Product_Taxable.

		:returns: bool
		"""

		return self.product_taxable

	def get_product_active(self) -> bool:
		"""
		Get Product_Active.

		:returns: bool
		"""

		return self.product_active

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_product_code(self, product_code: str) -> 'ProductInsert':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductInsert
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductInsert':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductInsert
		"""

		self.product_sku = product_sku
		return self

	def set_product_name(self, product_name: str) -> 'ProductInsert':
		"""
		Set Product_Name.

		:param product_name: str
		:returns: ProductInsert
		"""

		self.product_name = product_name
		return self

	def set_product_description(self, product_description: str) -> 'ProductInsert':
		"""
		Set Product_Description.

		:param product_description: str
		:returns: ProductInsert
		"""

		self.product_description = product_description
		return self

	def set_product_canonical_category_code(self, product_canonical_category_code: str) -> 'ProductInsert':
		"""
		Set Product_Canonical_Category_Code.

		:param product_canonical_category_code: str
		:returns: ProductInsert
		"""

		self.product_canonical_category_code = product_canonical_category_code
		return self

	def set_product_alternate_display_page(self, product_alternate_display_page: str) -> 'ProductInsert':
		"""
		Set Product_Alternate_Display_Page.

		:param product_alternate_display_page: str
		:returns: ProductInsert
		"""

		self.product_alternate_display_page = product_alternate_display_page
		return self

	def set_product_page_title(self, product_page_title: str) -> 'ProductInsert':
		"""
		Set Product_Page_Title.

		:param product_page_title: str
		:returns: ProductInsert
		"""

		self.product_page_title = product_page_title
		return self

	def set_product_thumbnail(self, product_thumbnail: str) -> 'ProductInsert':
		"""
		Set Product_Thumbnail.

		:param product_thumbnail: str
		:returns: ProductInsert
		"""

		self.product_thumbnail = product_thumbnail
		return self

	def set_product_image(self, product_image: str) -> 'ProductInsert':
		"""
		Set Product_Image.

		:param product_image: str
		:returns: ProductInsert
		"""

		self.product_image = product_image
		return self

	def set_product_price(self, product_price: float) -> 'ProductInsert':
		"""
		Set Product_Price.

		:param product_price: float
		:returns: ProductInsert
		"""

		self.product_price = product_price
		return self

	def set_product_cost(self, product_cost: float) -> 'ProductInsert':
		"""
		Set Product_Cost.

		:param product_cost: float
		:returns: ProductInsert
		"""

		self.product_cost = product_cost
		return self

	def set_product_weight(self, product_weight: float) -> 'ProductInsert':
		"""
		Set Product_Weight.

		:param product_weight: float
		:returns: ProductInsert
		"""

		self.product_weight = product_weight
		return self

	def set_product_inventory(self, product_inventory: int) -> 'ProductInsert':
		"""
		Set Product_Inventory.

		:param product_inventory: int
		:returns: ProductInsert
		"""

		self.product_inventory = product_inventory
		return self

	def set_product_taxable(self, product_taxable: bool) -> 'ProductInsert':
		"""
		Set Product_Taxable.

		:param product_taxable: bool
		:returns: ProductInsert
		"""

		self.product_taxable = product_taxable
		return self

	def set_product_active(self, product_active: bool) -> 'ProductInsert':
		"""
		Set Product_Active.

		:param product_active: bool
		:returns: ProductInsert
		"""

		self.product_active = product_active
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'ProductInsert':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: ProductInsert
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductInsert':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductInsert':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductInsert(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Product_Code'] = self.product_code
		data['Product_SKU'] = self.product_sku
		data['Product_Name'] = self.product_name
		if self.product_description is not None:
			data['Product_Description'] = self.product_description
		if self.product_canonical_category_code is not None:
			data['Product_Canonical_Category_Code'] = self.product_canonical_category_code
		if self.product_alternate_display_page is not None:
			data['Product_Alternate_Display_Page'] = self.product_alternate_display_page
		if self.product_page_title is not None:
			data['Product_Page_Title'] = self.product_page_title
		if self.product_thumbnail is not None:
			data['Product_Thumbnail'] = self.product_thumbnail
		if self.product_image is not None:
			data['Product_Image'] = self.product_image
		if self.product_price is not None:
			data['Product_Price'] = self.product_price
		if self.product_cost is not None:
			data['Product_Cost'] = self.product_cost
		if self.product_weight is not None:
			data['Product_Weight'] = self.product_weight
		if self.product_inventory is not None:
			data['Product_Inventory'] = self.product_inventory
		if self.product_taxable is not None:
			data['Product_Taxable'] = self.product_taxable
		if self.product_active is not None:
			data['Product_Active'] = self.product_active
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
