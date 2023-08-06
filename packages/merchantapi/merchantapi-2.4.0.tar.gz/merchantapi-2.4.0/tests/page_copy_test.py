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


def test_page_copy():
	"""
	Tests the Page_Copy API Call
	"""

	helper.provision_store('Page_Copy.xml')

	page_copy_test_copy()
	page_copy_test_copy_with_rules()


def page_copy_test_copy():
	check = helper.get_page('PageCopyTest_1_Copy')
	assert check == None

	request = merchantapi.request.PageCopy(helper.init_client())

	request.set_source_page_code('PageCopyTest_1')
	request.set_destination_page_code('PageCopyTest_1_Copy')
	request.set_destination_page_name('PageCopyTest_1_Copy')
	request.set_destination_page_create(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageCopy)

	check = helper.get_page('PageCopyTest_1_Copy')

	assert check is not None


def page_copy_test_copy_with_rules():
	check = helper.get_page('PageCopyTest_2_Copy')
	assert check == None

	request = merchantapi.request.PageCopy(helper.init_client())

	request.set_source_page_code('PageCopyTest_2')
	request.set_destination_page_code('PageCopyTest_2_Copy')
	request.set_destination_page_name('PageCopyTest_2_Copy')
	request.set_destination_page_create(True)
	request.set_copy_page_rules_name('PageCopyTest_Rules_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageCopy)

	check = helper.get_page('PageCopyTest_2_Copy')

	assert check is not None
