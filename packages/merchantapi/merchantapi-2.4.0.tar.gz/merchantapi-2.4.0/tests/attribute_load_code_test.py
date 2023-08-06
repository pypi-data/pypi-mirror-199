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


def test_attribute_load_code():
	"""
	Tests the Attribute_Load_Code API Call
	"""

	helper.provision_store('Attribute_Load_Code.xml')

	attribute_load_code_test_load()


def attribute_load_code_test_load():
	request = merchantapi.request.AttributeLoadCode(helper.init_client())

	request.set_product_code('AttributeLoadCodeTest_1')
	request.set_attribute_code('attr_choice')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeLoadCode)

	assert response.get_product_attribute() is not None
	assert response.get_product_attribute().get_code() is not None
