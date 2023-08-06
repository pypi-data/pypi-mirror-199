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


def test_option_insert():
	"""
	Tests the Option_Insert API Call
	"""

	helper.provision_store('Option_Insert.xml')

	option_insert_test_insertion()


def option_insert_test_insertion():
	options = helper.get_product_options('OptionInsertTest_1', 'OptionInsertTest_1')

	assert len(options) == 0

	request = merchantapi.request.OptionInsert(helper.init_client())

	request.set_product_code('OptionInsertTest_1')
	request.set_attribute_code('OptionInsertTest_1')
	request.set_code('OptionInsertTest_1')
	request.set_prompt('OptionInsertTest_1')
	request.set_image('')
	request.set_price(5.00)
	request.set_cost(2.2)
	request.set_weight(1.1)
	request.set_default(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionInsert)

	assert isinstance(response.get_product_option(), merchantapi.model.ProductOption)
	assert response.get_product_option().get_code() == 'OptionInsertTest_1'
	assert response.get_product_option().get_prompt() == 'OptionInsertTest_1'
	assert response.get_product_option().get_image() == ''
	assert response.get_product_option().get_price() == 5.00
	assert response.get_product_option().get_cost() == 2.2
	assert response.get_product_option().get_weight() == 1.1

	check_options = helper.get_product_options('OptionInsertTest_1', 'OptionInsertTest_1')

	assert len(check_options) == 1
	assert check_options[0].get_id() == response.get_product_option().get_id()
