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


def test_product_kit_update_parts():
	"""
	Tests the ProductKit_Update_Parts API Call
	"""

	helper.provision_store('ProductKit_Update_Parts.xml')

	product_kit_update_parts_test_update()


def product_kit_update_parts_test_update():
	product = helper.get_product('ProductKitUpdatePartsTest_1')

	assert product is not None
	assert len(product.get_attributes()) == 2

	p = 0
	for a in product.get_attributes():
		for o in a.get_options():
			p = p + 1
			part_product = helper.get_product('ProductKitUpdatePartsTest_1_%d' % p)

			assert part_product is not None

			request = merchantapi.request.ProductKitUpdateParts(helper.init_client(), product)

			request.set_attribute_id(a.get_id())
			request.set_option_id(o.get_id())

			part = merchantapi.model.KitPart()

			part.set_part_id(part_product.get_id())
			part.set_quantity(1)

			request.add_kit_part(part)

			response = request.send()

			helper.validate_response_success(response, merchantapi.response.ProductKitUpdateParts)

	assert p > 0
