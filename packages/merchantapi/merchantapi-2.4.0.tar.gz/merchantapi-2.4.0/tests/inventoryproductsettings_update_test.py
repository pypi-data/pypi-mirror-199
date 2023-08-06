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


def test_inventory_product_settings_update():
	"""
	Tests the InventoryProductSettings_Update API Call
	"""

	helper.provision_store('InventoryProductSettings_Update.xml')

	inventory_product_settings_update_test_update()


def inventory_product_settings_update_test_update():
	product = helper.get_product('InventoryProductSettingsUpdateTest_1');

	assert product is not None

	request = merchantapi.request.InventoryProductSettingsUpdate(helper.init_client(), product)

	request.set_track_product(True)
	request.set_track_low_stock_level("Yes")
	request.set_track_out_of_stock_level("Yes")
	request.set_hide_out_of_stock_products("Yes")
	request.set_in_stock_message_short("It is in stock")
	request.set_in_stock_message_long("Stop complaining, we can ship it right now")
	request.set_low_stock_message_short("Speak now")
	request.set_low_stock_message_long("Or forever hold your peace")
	request.set_out_of_stock_message_short("Sucker")
	request.set_out_of_stock_message_long("We sold out because you waited too long")
	request.set_limited_stock_message("We have of the limited")
	request.set_current_stock(12);

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.InventoryProductSettingsUpdate)

	check = helper.get_product(product.get_code());

	assert check.get_product_inventory_settings().get_in_stock_message_short() ==  "It is in stock"
	assert check.get_product_inventory_settings().get_in_stock_message_long() ==  "Stop complaining, we can ship it right now"
	assert check.get_product_inventory_settings().get_low_stock_message_short() ==  "Speak now"
	assert check.get_product_inventory_settings().get_low_stock_message_long() ==  "Or forever hold your peace"
	assert check.get_product_inventory_settings().get_out_of_stock_message_short() ==  "Sucker"
	assert check.get_product_inventory_settings().get_out_of_stock_message_long() ==  "We sold out because you waited too long"
	assert check.get_product_inventory_settings().get_limited_stock_message() ==  "We have of the limited"
