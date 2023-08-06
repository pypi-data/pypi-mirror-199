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


def test_print_queue_job_delete():
	"""
	Tests the PrintQueueJob_Delete API Call
	"""

	print_queue_job_delete_test_deletion()


def print_queue_job_delete_test_deletion():
	helper.create_print_queue('PrintQueueJobDeleteTest')

	insert_request = merchantapi.request.PrintQueueJobInsert(helper.init_client())

	insert_request.set_edit_print_queue('PrintQueueJobDeleteTest') \
		.set_print_queue_description('Description') \
		.set_print_queue_job_format('Format') \
		.set_print_queue_job_data('Data')

	insert_response = insert_request.send()

	helper.validate_response_success(insert_response, merchantapi.response.PrintQueueJobInsert)

	assert insert_response.get_print_queue_job() is not None
	assert insert_response.get_print_queue_job().get_id() > 0

	request = merchantapi.request.PrintQueueJobDelete(helper.init_client())

	request.set_print_queue_job_id(insert_response.get_print_queue_job().get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobDelete)
