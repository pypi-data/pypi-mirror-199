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


def test_print_queue_job_list_load_query():
	"""
	Tests the PrintQueueJobList_Load_Query API Call
	"""

	print_queue_job_list_load_query_test_list_load()
	print_queue_job_list_load_query_test_invalid_queue()


def print_queue_job_list_load_query_test_list_load():
	helper.create_print_queue('PrintQueueJobListLoadQueryTest')

	request = merchantapi.request.PrintQueueJobListLoadQuery(helper.init_client())

	request.set_edit_print_queue('PrintQueueJobListLoadQueryTest')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobListLoadQuery)

	assert isinstance(response.get_print_queue_jobs(), list)

	for pqj in response.get_print_queue_jobs():
		assert isinstance(pqj, merchantapi.model.PrintQueueJob)


def print_queue_job_list_load_query_test_invalid_queue():
	request = merchantapi.request.PrintQueueJobListLoadQuery(helper.init_client())

	request.set_edit_print_queue('InvalidPrintQueue')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.PrintQueueJobListLoadQuery)
