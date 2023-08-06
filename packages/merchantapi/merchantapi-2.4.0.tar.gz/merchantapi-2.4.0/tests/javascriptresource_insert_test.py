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


def test_javascriptresource_insert():
	"""
	Tests the JavaScriptResource_Insert API Call
	"""

	helper.reset_branch_state()
	helper.provision_store('JavaScriptResource_Insert.xml')

	javascriptresource_insert_test_insertion_inline()
	javascriptresource_insert_test_insertion_external()
	javascriptresource_insert_test_insertion_local()
	javascriptresource_insert_test_insertion_combined()


def javascriptresource_insert_test_insertion_inline():
	request = merchantapi.request.JavaScriptResourceInsert(helper.init_client())

	request.set_javascript_resource_code('JavaScriptResource_Insert_1')
	request.set_javascript_resource_type(merchantapi.model.JavaScriptResource.RESOURCE_TYPE_INLINE)
	request.set_javascript_resource_global(False)
	request.set_javascript_resource_active(True)

	attribute = merchantapi.model.JavaScriptResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_javascript_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceInsert)
	
	assert response.get_javascript_resource() is not None
	assert response.get_javascript_resource().get_id() > 0
	assert response.get_javascript_resource().get_code() == 'JavaScriptResource_Insert_1'
	assert response.get_javascript_resource().get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_INLINE
	assert response.get_javascript_resource().get_is_global() == False
	assert response.get_javascript_resource().get_active() == True

	check = helper.get_javascript_resource('JavaScriptResource_Insert_1')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'JavaScriptResource_Insert_1'
	assert check.get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_INLINE
	assert check.get_is_global() == False
	assert check.get_active() == True


def javascriptresource_insert_test_insertion_external():
	request = merchantapi.request.JavaScriptResourceInsert(helper.init_client())

	request.set_javascript_resource_code('JavaScriptResource_Insert_2')
	request.set_javascript_resource_type(merchantapi.model.JavaScriptResource.RESOURCE_TYPE_EXTERNAL)
	request.set_javascript_resource_file_path('https://www.coolcommerce.net/some/external/resource.js')
	request.set_javascript_resource_global(False)
	request.set_javascript_resource_active(True)

	attribute = merchantapi.model.JavaScriptResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_javascript_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceInsert)

	assert response.get_javascript_resource() is not None
	assert response.get_javascript_resource().get_id() > 0
	assert response.get_javascript_resource().get_code() == 'JavaScriptResource_Insert_2'
	assert response.get_javascript_resource().get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_EXTERNAL
	assert response.get_javascript_resource().get_file() == 'https://www.coolcommerce.net/some/external/resource.js'
	assert response.get_javascript_resource().get_is_global() == False
	assert response.get_javascript_resource().get_active() == True

	check = helper.get_javascript_resource('JavaScriptResource_Insert_2')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'JavaScriptResource_Insert_2'
	assert check.get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_EXTERNAL
	assert check.get_file() == 'https://www.coolcommerce.net/some/external/resource.js'
	assert check.get_is_global() == False
	assert check.get_active() == True


def javascriptresource_insert_test_insertion_local():
	request = merchantapi.request.JavaScriptResourceInsert(helper.init_client())

	request.set_javascript_resource_code('JavaScriptResource_Insert_3')
	request.set_javascript_resource_type(merchantapi.model.JavaScriptResource.RESOURCE_TYPE_LOCAL)
	request.set_javascript_resource_file_path('some/local/resource.js')
	request.set_javascript_resource_global(False)
	request.set_javascript_resource_active(True)

	attribute = merchantapi.model.JavaScriptResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_javascript_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceInsert)
	
	assert response.get_javascript_resource() is not None
	assert response.get_javascript_resource().get_id() > 0
	assert response.get_javascript_resource().get_code() == 'JavaScriptResource_Insert_3'
	assert response.get_javascript_resource().get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_LOCAL
	assert response.get_javascript_resource().get_file() == 'some/local/resource.js'
	assert response.get_javascript_resource().get_is_global() == False
	assert response.get_javascript_resource().get_active() == True

	check = helper.get_javascript_resource('JavaScriptResource_Insert_3')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'JavaScriptResource_Insert_3'
	assert check.get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_LOCAL
	assert check.get_file() == 'some/local/resource.js'
	assert check.get_is_global() == False
	assert check.get_active() == True


def javascriptresource_insert_test_insertion_combined():
	request = merchantapi.request.JavaScriptResourceInsert(helper.init_client())

	request.set_javascript_resource_code('JavaScriptResource_Insert_4')
	request.set_javascript_resource_type(merchantapi.model.JavaScriptResource.RESOURCE_TYPE_COMBINED)
	request.set_javascript_resource_global(False)
	request.set_javascript_resource_active(True)

	attribute = merchantapi.model.JavaScriptResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_javascript_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.JavaScriptResourceInsert)

	assert response.get_javascript_resource() is not None
	assert response.get_javascript_resource().get_id() > 0
	assert response.get_javascript_resource().get_code() == 'JavaScriptResource_Insert_4'
	assert response.get_javascript_resource().get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_COMBINED
	assert response.get_javascript_resource().get_is_global() == False
	assert response.get_javascript_resource().get_active() == True

	check = helper.get_javascript_resource('JavaScriptResource_Insert_4')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'JavaScriptResource_Insert_4'
	assert check.get_type() == merchantapi.model.JavaScriptResource.RESOURCE_TYPE_COMBINED
	assert check.get_is_global() == False
	assert check.get_active() == True
