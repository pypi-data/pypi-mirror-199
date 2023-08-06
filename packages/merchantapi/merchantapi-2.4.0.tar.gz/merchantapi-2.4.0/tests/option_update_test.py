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


def test_option_update():
	"""
	Tests the Option_Update API Call
	"""

	helper.provision_store('Option_Update.xml')

	option_update_test_update()


def option_update_test_update():
	attribute = helper.get_product_attribute('OptionUpdateTest_1', 'OptionUpdateTest_1')
	options = helper.get_product_options('OptionUpdateTest_1', 'OptionUpdateTest_1')

	assert attribute is not None
	assert len(options) == 1

	request = merchantapi.request.OptionUpdate(helper.init_client())

	request.set_product_code('OptionUpdateTest_1')
	request.set_option_code('OptionUpdateTest_1')
	request.set_attribute_id(attribute.get_id())
	request.set_prompt('OptionUpdateTest_1 Updated')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionUpdate)

	check_options = helper.get_product_options('OptionUpdateTest_1', 'OptionUpdateTest_1')

	assert len(check_options) == 1
	assert check_options[0].get_prompt() == 'OptionUpdateTest_1 Updated'
