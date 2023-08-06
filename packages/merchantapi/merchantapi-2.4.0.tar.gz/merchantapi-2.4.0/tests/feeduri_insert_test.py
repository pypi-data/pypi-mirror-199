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


def test_feed_uri_insert():
	"""
	Tests the FeedURI_Insert API Call
	"""

	helper.provision_store('FeedURI_Insert.xml')

	feed_uri_insert_test_insertion()


def feed_uri_insert_test_insertion():
	test_uri = '/FeedURIInsertTest_1_INSERTED'

	request = merchantapi.request.FeedURIInsert(helper.init_client())

	request.set_uri(test_uri)
	request.set_feed_code('FeedURIInsertTest_1')
	request.set_canonical(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIInsert)

	assert isinstance(response.get_uri(), merchantapi.model.Uri)
	assert response.get_uri().get_uri() == test_uri

	check = helper.get_feed_uris('FeedURIInsertTest_1')

	assert len(check) == 1
	assert check[0].get_uri() == test_uri
