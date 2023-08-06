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


def test_option_load_code():
	"""
	Tests the Option_Load_Code API Call
	"""

	helper.provision_store('Option_Load_Code.xml')

	option_load_code_test_load()


def option_load_code_test_load():
	request = merchantapi.request.OptionLoadCode(helper.init_client())

	request.set_product_code('OptionLoadCodeTest_1')
	request.set_attribute_code('OptionLoadCodeTest_1')
	request.set_option_code('OptionLoadCodeTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionLoadCode)

	assert response.get_product_option() is not None
	assert response.get_product_option().get_code() == 'OptionLoadCodeTest_1'
