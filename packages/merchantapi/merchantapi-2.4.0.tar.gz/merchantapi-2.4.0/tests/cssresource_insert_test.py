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


def test_cssresource_insert():
	"""
	Tests the CSSResource_Insert API Call
	"""

	helper.reset_branch_state()
	helper.provision_store('CSSResource_Insert.xml')

	cssresource_insert_test_insertion_inline()
	cssresource_insert_test_insertion_external()
	cssresource_insert_test_insertion_local()
	cssresource_insert_test_insertion_combined()


def cssresource_insert_test_insertion_inline():
	request = merchantapi.request.CSSResourceInsert(helper.init_client())

	request.set_css_resource_code('CSSResource_Insert_1')
	request.set_css_resource_type(merchantapi.model.CSSResource.RESOURCE_TYPE_INLINE)
	request.set_css_resource_global(False)
	request.set_css_resource_active(True)

	attribute = merchantapi.model.CSSResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_css_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceInsert)

	assert response.get_css_resource() is not None
	assert response.get_css_resource().get_id() > 0
	assert response.get_css_resource().get_code() == 'CSSResource_Insert_1'
	assert response.get_css_resource().get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_INLINE
	assert response.get_css_resource().get_is_global() == False
	assert response.get_css_resource().get_active() == True

	check = helper.get_css_resource('CSSResource_Insert_1')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'CSSResource_Insert_1'
	assert check.get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_INLINE
	assert check.get_is_global() == False
	assert check.get_active() == True


def cssresource_insert_test_insertion_external():
	request = merchantapi.request.CSSResourceInsert(helper.init_client())

	request.set_css_resource_code('CSSResource_Insert_2')
	request.set_css_resource_type(merchantapi.model.CSSResource.RESOURCE_TYPE_EXTERNAL)
	request.set_css_resource_file_path('https://www.coolcommerce.net/some/external/resource.css')
	request.set_css_resource_global(False)
	request.set_css_resource_active(True)

	attribute = merchantapi.model.CSSResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_css_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceInsert)

	assert response.get_css_resource() is not None
	assert response.get_css_resource().get_id() > 0
	assert response.get_css_resource().get_code() == 'CSSResource_Insert_2'
	assert response.get_css_resource().get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_EXTERNAL
	assert response.get_css_resource().get_file() == 'https://www.coolcommerce.net/some/external/resource.css'
	assert response.get_css_resource().get_is_global() == False
	assert response.get_css_resource().get_active() == True

	check = helper.get_css_resource('CSSResource_Insert_2')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'CSSResource_Insert_2'
	assert check.get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_EXTERNAL
	assert check.get_file() == 'https://www.coolcommerce.net/some/external/resource.css'
	assert check.get_is_global() == False
	assert check.get_active() == True


def cssresource_insert_test_insertion_local():
	request = merchantapi.request.CSSResourceInsert(helper.init_client())

	request.set_css_resource_code('CSSResource_Insert_3')
	request.set_css_resource_type(merchantapi.model.CSSResource.RESOURCE_TYPE_LOCAL)
	request.set_css_resource_file_path('some/local/resource.css')
	request.set_css_resource_global(False)
	request.set_css_resource_active(True)

	attribute = merchantapi.model.CSSResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_css_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceInsert)

	assert response.get_css_resource() is not None
	assert response.get_css_resource().get_id() > 0
	assert response.get_css_resource().get_code() == 'CSSResource_Insert_3'
	assert response.get_css_resource().get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_LOCAL
	assert response.get_css_resource().get_file() == 'some/local/resource.css'
	assert response.get_css_resource().get_is_global() == False
	assert response.get_css_resource().get_active() == True

	check = helper.get_css_resource('CSSResource_Insert_3')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'CSSResource_Insert_3'
	assert check.get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_LOCAL
	assert check.get_file() == 'some/local/resource.css'
	assert check.get_is_global() == False
	assert check.get_active() == True


def cssresource_insert_test_insertion_combined():
	request = merchantapi.request.CSSResourceInsert(helper.init_client())

	request.set_css_resource_code('CSSResource_Insert_4')
	request.set_css_resource_type(merchantapi.model.CSSResource.RESOURCE_TYPE_COMBINED)
	request.set_css_resource_global(False)
	request.set_css_resource_active(True)

	attribute = merchantapi.model.CSSResourceAttribute()
	attribute.set_name('foo')
	attribute.set_value('bar')

	request.add_css_resource_attribute(attribute)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CSSResourceInsert)

	assert response.get_css_resource() is not None
	assert response.get_css_resource().get_id() > 0
	assert response.get_css_resource().get_code() == 'CSSResource_Insert_4'
	assert response.get_css_resource().get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_COMBINED
	assert response.get_css_resource().get_is_global() == False
	assert response.get_css_resource().get_active() == True

	check = helper.get_css_resource('CSSResource_Insert_4')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'CSSResource_Insert_4'
	assert check.get_type() == merchantapi.model.CSSResource.RESOURCE_TYPE_COMBINED
	assert check.get_is_global() == False
	assert check.get_active() == True
