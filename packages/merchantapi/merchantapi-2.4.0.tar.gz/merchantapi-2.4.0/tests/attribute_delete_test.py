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


def test_attribute_delete():
	"""
	Tests the Attribute_Delete API Call
	"""

	helper.provision_store('Attribute_Delete.xml')

	attribute_delete_test_deletion()


def attribute_delete_test_deletion():
	request = merchantapi.request.AttributeDelete(helper.init_client())

	request.set_product_code('AttributeDeleteTest_1')
	request.set_attribute_code('AttributeDeleteTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeDelete)

	check = helper.get_product_attribute('AttributeDeleteTest_1', 'AttributeDeleteTest_1')

	assert check is None
