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


def test_attribute_copy_template():
	"""
	Tests the Attribute_CopyTemplate API Call
	"""

	helper.provision_store('Attribute_CopyTemplate.xml')

	attribute_copy_template_test_copy()


def attribute_copy_template_test_copy():
	check = helper.get_product('AttributeCopyTemplate')
	
	assert check is not None
	assert len(check.get_attributes()) == 0

	request = merchantapi.request.AttributeCopyTemplate(helper.init_client())

	request.set_product_code('AttributeCopyTemplate')
	request.set_attribute_template_code('AttributeCopyTemplate')

	response = request.send()

	check = helper.get_attribute_template('AttributeCopyTemplate')

	assert check is not None
	assert check.get_code() == 'AttributeCopyTemplate'
