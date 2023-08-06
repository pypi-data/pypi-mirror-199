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


def test_attribute_update():
	"""
	Tests the Attribute_Update API Call
	"""

	helper.provision_store('Attribute_Update.xml')

	attribute_update_test_update()


def attribute_update_test_update():
	request = merchantapi.request.AttributeUpdate(helper.init_client())

	request.set_product_code('AttributeUpdateTest_1')
	request.set_attribute_code('AttributeUpdateTest_1')
	request.set_prompt('AttributeUpdateTest_1_Updated')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeUpdate)

	check = helper.get_product_attribute('AttributeUpdateTest_1', 'AttributeUpdateTest_1')

	assert check is not None
	assert check.get_prompt() == 'AttributeUpdateTest_1_Updated'
