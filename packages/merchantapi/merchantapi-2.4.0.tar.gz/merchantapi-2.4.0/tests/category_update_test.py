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


def test_category_update():
	"""
	Tests the Category_Update API Call
	"""

	helper.provision_store('Category_Update.xml')

	category_update_test_update()


def category_update_test_update():
	request = merchantapi.request.CategoryUpdate(helper.init_client())

	request.set_edit_category('CategoryUpdateTest_01')\
		.set_category_name('CategoryUpdateTest_01 New Name')\
		.set_category_active(False)\
		.set_category_page_title('CategoryUpdateTest_01 New Page Title')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryUpdate)

	check = helper.get_category('CategoryUpdateTest_01')

	assert check is not None
	assert check.get_code() == 'CategoryUpdateTest_01'
	assert check.get_name() == 'CategoryUpdateTest_01 New Name'
	assert check.get_page_title() == 'CategoryUpdateTest_01 New Page Title'
	assert check.get_active() is False
