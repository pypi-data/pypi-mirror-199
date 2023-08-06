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


def test_feed_uri_update():
	"""
	Tests the FeedURI_Update API Call
	"""

	helper.provision_store('FeedURI_Update.xml')

	feed_uri_update_test_update()


def feed_uri_update_test_update():
	uris = helper.get_feed_uris('FeedURIUpdateTest_1')

	assert len(uris) == 1

	test_uri = uris[0].get_uri() + '_UPDATED'

	request = merchantapi.request.FeedURIUpdate(helper.init_client(), uris[0])

	request.set_uri(test_uri)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIUpdate)

	check = helper.get_feed_uris('FeedURIUpdateTest_1')

	assert len(check) == 1
	assert check[0].get_uri() == test_uri
