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


def test_feed_uri_list_delete():
	"""
	Tests the FeedURIList_Delete API Call
	"""

	helper.provision_store('FeedURIList_Delete.xml')

	feed_uri_list_delete_test_deletion()


def feed_uri_list_delete_test_deletion():
	uris = helper.get_feed_uris('FeedURIListDeleteTest_1')

	assert uris is not None
	assert len(uris) == 8

	request = merchantapi.request.FeedURIListDelete(helper.init_client())

	for u in uris:
		if not u.get_canonical():
			request.add_uri(u)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.FeedURIListDelete)

	check = helper.get_feed_uris('FeedURIListDeleteTest_1')

	assert len(check) == 0
