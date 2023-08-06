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


def test_option_delete():
	"""
	Tests the Option_Delete API Call
	"""

	helper.provision_store('Option_Delete.xml')

	option_delete_test_deletion()


def option_delete_test_deletion():
	attribute = helper.get_product_attribute('OptionDeleteTest_1', 'OptionDeleteTest_1')
	options = helper.get_product_options('OptionDeleteTest_1', 'OptionDeleteTest_1')

	assert attribute is not None
	assert len(options) == 2

	request = merchantapi.request.OptionDelete(helper.init_client())

	request.set_option_code('OptionDeleteTest_1')
	request.set_attribute_id(attribute.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionDelete)

	check_options = helper.get_product_options('OptionDeleteTest_1', 'OptionDeleteTest_1')

	assert len(check_options) == 1
