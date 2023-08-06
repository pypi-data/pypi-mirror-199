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


def test_print_queue_list_load_query():
	"""
	Tests the PrintQueueList_Load_Query API Call
	"""

	print_queue_list_load_query_test_list_load()


def print_queue_list_load_query_test_list_load():
	request = merchantapi.request.PrintQueueListLoadQuery(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueListLoadQuery)

	assert isinstance(response.get_print_queues(), list)

	for pq in response.get_print_queues():
		assert isinstance(pq, merchantapi.model.PrintQueue)
