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


def test_category_list_load_query():
	"""
	Tests the CategoryList_Load_Query API Call
	"""

	helper.provision_store('CategoryList_Load_Query.xml')
	helper.upload_image('graphics/CategoryListLoadQuery1.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery2.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery3.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery4.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery5.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery6.jpg')
	helper.upload_image('graphics/CategoryListLoadQuery7.jpg')

	category_list_load_query_test_list_load()
	category_list_load_query_test_list_load_with_custom_fields()


def category_list_load_query_test_list_load():
	request = merchantapi.request.CategoryListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'CategoryListLoadQueryTest_%'))

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryListLoadQuery)

	assert isinstance(response.get_categories(), list)
	assert len(response.get_categories()) == 7

	for i, category in enumerate(response.get_categories()):
		assert isinstance(category, merchantapi.model.Category)
		assert category.get_code() == 'CategoryListLoadQueryTest_%d' % int(i+1)
		assert category.get_name() == 'CategoryListLoadQueryTest_%d' % int(i+1)


def category_list_load_query_test_list_load_with_custom_fields():
	request = merchantapi.request.CategoryListLoadQuery(helper.init_client())

	request.set_filters(request.filter_expression().like('code', 'CategoryListLoadQueryTest_%'))\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_checkbox')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_imageupload')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_text')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_textarea')\
		.add_on_demand_column('CustomField_Values:customfields:CategoryListLoadQueryTest_dropdown')\
		.set_sort('code', merchantapi.request.CategoryListLoadQuery.SORT_ASCENDING)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CategoryListLoadQuery)

	assert isinstance(response.get_categories(), list)
	assert len(response.get_categories()) == 7

	for i, category in enumerate(response.get_categories()):
		assert isinstance(category, merchantapi.model.Category)
		assert category.get_code() == 'CategoryListLoadQueryTest_%d' % int(i+1)
		assert category.get_name() == 'CategoryListLoadQueryTest_%d' % int(i+1)

		assert isinstance(category.get_custom_field_values(), merchantapi.model.CustomFieldValues)

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_checkbox', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_checkbox', 'customfields') == '1'

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_imageupload', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_imageupload', 'customfields') == 'graphics/00000001/CategoryListLoadQuery%d.jpg' % int(i+1)

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_text', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_text', 'customfields') == 'CategoryListLoadQueryTest_%d' % int(i+1)

		assert category.get_custom_field_values().has_value('CategoryListLoadQueryTest_dropdown', 'customfields') is True
		assert category.get_custom_field_values().get_value('CategoryListLoadQueryTest_dropdown', 'customfields') == 'Option%d' % int(i+1)
