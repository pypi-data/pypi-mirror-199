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


def test_print_queue_job_insert():
	"""
	Tests the PrintQueueJob_Insert API Call
	"""

	print_queue_job_insert_test_insertion()


def print_queue_job_insert_test_insertion():
	helper.create_print_queue('PrintQueueJobInsertTest')

	request = merchantapi.request.PrintQueueJobInsert(helper.init_client())

	request.set_edit_print_queue('PrintQueueJobInsertTest') \
		.set_print_queue_job_description('Description') \
		.set_print_queue_job_format('Format') \
		.set_print_queue_job_data('Data')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PrintQueueJobInsert)

	assert isinstance(response.get_print_queue_job(), merchantapi.model.PrintQueueJob)

	assert response.get_print_queue_job().get_id() > 0
	assert response.get_print_queue_job().get_description() == 'Description'
	assert response.get_print_queue_job().get_job_format() == 'Format'
	assert response.get_print_queue_job().get_job_data() == 'Data'
