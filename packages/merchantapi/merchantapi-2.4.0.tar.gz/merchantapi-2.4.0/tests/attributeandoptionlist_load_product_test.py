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


def test_attribute_and_option_list_load_product():
	"""
	Tests the AttributeAndOptionList_Load_Product API Call
	"""

	helper.provision_store('AttributeAndOptionList_Load_Product.xml')

	attribute_and_option_list_load_product_test_list_load()


def attribute_and_option_list_load_product_test_list_load():
	request = merchantapi.request.AttributeAndOptionListLoadProduct(helper.init_client())

	request.set_product_code('AttributeAndOptionListLoadProductTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeAndOptionListLoadProduct)

	assert len(response.get_product_attributes()) == 3

	valid_codes = [
		'AttributeAndOptionListLoadProductTest_1',
		'AttributeAndOptionListLoadProductTest_2',
		'AttributeAndOptionListLoadProductTest_3'
	]

	for a in response.get_product_attributes():
		assert a.get_code() in valid_codes
		assert len(a.get_options()) == 3

		for o in a.get_options():
			assert o.get_code() in valid_codes
