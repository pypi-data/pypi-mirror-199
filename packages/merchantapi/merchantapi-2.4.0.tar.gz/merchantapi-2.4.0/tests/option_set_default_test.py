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


def test_option_set_default():
	"""
	Tests the Option_Set_Default API Call
	"""

	helper.provision_store('Option_Set_Default.xml')

	option_set_default_test_set()


def option_set_default_test_set():
	attribute = helper.get_product_attribute('OptionSetDefaultTest_1', 'OptionSetDefaultTest_1')

	assert attribute is not None

	request = merchantapi.request.OptionSetDefault(helper.init_client())

	request.set_attribute_id(attribute.get_id())
	request.set_option_code('OptionSetDefaultTest_2')
	request.set_option_default(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OptionSetDefault)

	check_attribute = helper.get_product_attribute('OptionSetDefaultTest_1', 'OptionSetDefaultTest_1')
	check_option = None

	for o in helper.get_product_options('OptionSetDefaultTest_1', 'OptionSetDefaultTest_1'):
		if o.get_code() == 'OptionSetDefaultTest_2':
			check_option = o
			break

	assert check_option is not None
	assert check_attribute.get_default_id() == check_option.get_id()
