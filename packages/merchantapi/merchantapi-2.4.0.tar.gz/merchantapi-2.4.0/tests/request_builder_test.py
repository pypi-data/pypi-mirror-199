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


def test_request_builder():
	"""
	Tests the RequestBuilder functionality
	"""

	helper.provision_store('ProductList_Load_Query.xml')

	test_request_builder_get_set()
	test_request_builder_function()
	test_list_query_request_builder_function()


def test_request_builder_get_set():
	request = merchantapi.request.RequestBuilder(helper.init_client(), 'Function', { 'foo': 'bar' })

	request.set_store_code('Store_Code')
	request.set('bar', 'foo')

	assert request.function == 'Function'
	assert request.store_code == 'Store_Code'
	assert request.get('foo') == 'bar'
	assert request.get('bar') == 'foo'


def test_request_builder_function():
	request = merchantapi.request.RequestBuilder(helper.init_client())

	request.set_function('ProductList_Load_Query')
	request.set('Count', 1)
	
	response = request.send()
	helper.validate_response_success(response, merchantapi.response.RequestBuilder)

	assert isinstance(response.get_data(), dict)
	assert isinstance(response.get_data()['data'], dict)
	assert isinstance(response.get_data()['data']['data'], list)
	assert len(response.get_data()['data']['data']) == 1


def test_list_query_request_builder_function():
	request = merchantapi.request.ListQueryRequestBuilder(helper.init_client())

	request.set_function('ProductList_Load_Query')
	request.set_count(1)
	
	response = request.send()
	helper.validate_response_success(response, merchantapi.response.ListQueryRequestBuilder)

	assert isinstance(response.get_data(), dict)
	assert isinstance(response.get_data()['data'], dict)
	assert isinstance(response.get_data()['data']['data'], list)
	assert len(response.get_data()['data']['data']) == 1
