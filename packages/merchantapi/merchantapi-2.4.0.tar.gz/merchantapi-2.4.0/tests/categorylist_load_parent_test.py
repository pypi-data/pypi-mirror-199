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


def test_category_list_load_parent():
	"""
	Tests the CategoryList_Load_Parent API Call
	"""

	helper.provision_store('CategoryList_Load_Parent.xml')

	category_list_load_parent_test_list_load()


def category_list_load_parent_test_list_load():
	parentcat = helper.get_category('CategoryListLoadParentTest_Parent')

	assert parentcat is not None
	assert isinstance(parentcat, merchantapi.model.Category)

	request = merchantapi.request.CategoryListLoadParent(helper.init_client(), parentcat)

	assert request.get_parent_id() == parentcat.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryListLoadParent)

	assert len(response.get_categories()) == 3

	for i, category in enumerate(response.get_categories()):
		assert isinstance(category, merchantapi.model.Category)
		assert category.get_code() == 'CategoryListLoadParentTest_Child_%d' % int(i+1)
		assert category.get_name() == 'CategoryListLoadParentTest_Child_%d' % int(i+1)
		assert category.get_active() is True
