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


def test_print_queue_job_status():
	"""
	Tests the PrintQueueJob_Status API Call
	"""

	print_queue_job_status_test_get_status()


def print_queue_job_status_test_get_status():
	helper.create_print_queue('PrintQueueJobStatusTest')

	insert_request = merchantapi.request.PrintQueueJobInsert(helper.init_client())

	insert_request.set_edit_print_queue('PrintQueueJobStatusTest') \
		.set_print_queue_description('Description') \
		.set_print_queue_job_format('Format') \
		.set_print_queue_job_data('Data')

	insert_response = insert_request.send()

	helper.validate_response_success(insert_response, merchantapi.response.PrintQueueJobInsert)

	assert insert_response.get_print_queue_job() is not None
	assert insert_response.get_print_queue_job().get_id() > 0

	request = merchantapi.request.PrintQueueJobStatus(helper.init_client())

	request.set_print_queue_job_id(insert_response.get_print_queue_job().get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobStatus)

	assert response.get_status() not in (None, '')
