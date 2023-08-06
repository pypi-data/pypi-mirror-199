"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
from . import helper


def test_product_list_adjust_inventory():
	"""
	Tests the ProductList_Adjust_Inventory API Call
	"""

	helper.provision_store('ProductList_Adjust_Inventory.xml')

	product_list_adjust_inventory_test_adjustment()


def product_list_adjust_inventory_test_adjustment():
	product = helper.get_product('ProductListAdjustInventoryTest_1')

	request = merchantapi.request.ProductListAdjustInventory(helper.init_client())
	adjustment = merchantapi.model.ProductInventoryAdjustment()

	adjustment.set_product_id(product.get_id()) \
		.set_adjustment(100)

	request.add_inventory_adjustment(adjustment)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductListAdjustInventory)
