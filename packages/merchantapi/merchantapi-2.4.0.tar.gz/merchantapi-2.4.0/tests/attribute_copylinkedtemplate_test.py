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


def test_attribute_copy_linked_template():
	"""
	Tests the Attribute_CopyLinkedTemplate API Call
	"""

	helper.provision_store('Attribute_CopyLinkedTemplate.xml')

	attribute_copy_linked_template_test_copy()


def attribute_copy_linked_template_test_copy():
	request = merchantapi.request.AttributeCopyLinkedTemplate(helper.init_client())

	request.set_product_code('AttributeCopyLinkedTemplate')
	request.set_attribute_code('AttributeCopyLinkedTemplate')

	response = request.send()

	check = helper.get_attribute_template('AttributeCopyLinkedTemplate')

	assert check != None
