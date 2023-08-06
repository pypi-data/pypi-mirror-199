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


def test_category_delete():
	"""
	Tests the Category_Delete API Call
	"""

	helper.provision_store('Category_Delete.xml')

	category_delete_test_deletion()
	category_delete_test_invalid_category()


def category_delete_test_deletion():
	request = merchantapi.request.CategoryDelete(helper.init_client())

	request.set_edit_category('CategoryDeleteTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryDelete)

	check = helper.get_category('CategoryDelete')
	assert check is None


def category_delete_test_invalid_category():
	request = merchantapi.request.CategoryDelete(helper.init_client())

	request.set_edit_category('InvalidCategory')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.CategoryDelete)
