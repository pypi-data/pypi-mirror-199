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


def test_category_insert():
	"""
	Tests the Category_Insert API Call
	"""

	helper.provision_store('Category_Insert.xml')

	category_insert_test_insertion()
	category_insert_test_insertion_with_custom_fields()


def category_insert_test_insertion():
	request = merchantapi.request.CategoryInsert(helper.init_client())

	request.set_category_code('CategoryInsertTest_1')\
		.set_category_name('CategoryInsertTest_1 Name')\
		.set_category_page_title('CategoryInsertTest_1 Page Title')\
		.set_category_active(True)\
		.set_category_parent_category('')\
		.set_category_alternate_display_page('')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryInsert)

	assert isinstance(response.get_category(), merchantapi.model.Category)
	assert response.get_category().get_code() == 'CategoryInsertTest_1'
	assert response.get_category().get_name() == 'CategoryInsertTest_1 Name'
	assert response.get_category().get_page_title() == 'CategoryInsertTest_1 Page Title'
	assert response.get_category().get_active() is True
	assert response.get_category().get_id() > 0

	check = helper.get_category('CategoryInsertTest_1')

	assert isinstance(check, merchantapi.model.Category)
	assert check.get_id() == response.get_category().get_id()


def category_insert_test_insertion_with_custom_fields():
	request = merchantapi.request.CategoryInsert(helper.init_client())

	request.set_category_code('CategoryInsertTest_2')\
		.set_category_name('CategoryInsertTest_2 Name')\
		.set_category_page_title('CategoryInsertTest_2 Page Title')\
		.set_category_active(True)\
		.set_category_parent_category('')\
		.set_category_alternate_display_page('')

	request.get_custom_field_values() \
		.add_value('CategoryInsertTest_checkbox', 'True', 'customfields') \
		.add_value('CategoryInsertTest_imageupload', 'graphics/00000001/CategoryInsert.jpg', 'customfields') \
		.add_value('CategoryInsertTest_text', 'CategoryInsertTest_2', 'customfields') \
		.add_value('CategoryInsertTest_textarea', 'CategoryInsertTest_2', 'customfields') \
		.add_value('CategoryInsertTest_dropdown', 'Option2', 'customfields')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryInsert)
	assert isinstance(response.get_category(), merchantapi.model.Category)

	check = helper.get_category('CategoryInsertTest_2')

	assert isinstance(check, merchantapi.model.Category)
	assert check.get_code() == 'CategoryInsertTest_2'
	assert check.get_name() == 'CategoryInsertTest_2 Name'
	assert check.get_page_title() == 'CategoryInsertTest_2 Page Title'
	assert check.get_active() is True
	assert check.get_id() > 0

	assert isinstance(check.get_custom_field_values(), merchantapi.model.CustomFieldValues)

	assert check.get_custom_field_values().has_value('CategoryInsertTest_checkbox', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_checkbox', 'customfields') == '1'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_imageupload', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_imageupload', 'customfields') == 'graphics/00000001/CategoryInsert.jpg'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_text', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_text', 'customfields') == 'CategoryInsertTest_2'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_textarea', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_textarea', 'customfields') == 'CategoryInsertTest_2'

	assert check.get_custom_field_values().has_value('CategoryInsertTest_dropdown', 'customfields') is True
	assert check.get_custom_field_values().get_value('CategoryInsertTest_dropdown', 'customfields') == 'Option2'
