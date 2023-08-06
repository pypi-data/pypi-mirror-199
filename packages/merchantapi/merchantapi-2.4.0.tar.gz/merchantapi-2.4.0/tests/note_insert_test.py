"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
import time
from . import helper


def test_note_insert():
	"""
	Tests the Note_Insert API Call
	"""

	helper.provision_store('Note_Insert.xml')

	note_insert_test_insertion_by_customer()
	note_insert_test_insertion_by_order()
	note_insert_test_invalid_customer()
	note_insert_test_invalid_order()


def note_insert_test_insertion_by_customer():
	customer = helper.get_customer('NoteInsertTest_Customer')

	assert isinstance(customer, merchantapi.model.Customer)

	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_customer_id(customer.get_id())\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteInsert)
	
	assert isinstance(response.get_note(), merchantapi.model.Note)
	assert response.get_note().get_note_text() == request.get_note_text()
	assert response.get_note().get_customer_id() == request.get_customer_id()


def note_insert_test_insertion_by_order():
	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_order_id(592745)\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteInsert)
	
	assert isinstance(response.get_note(), merchantapi.model.Note)
	assert response.get_note().get_note_text() == request.get_note_text()
	assert response.get_note().get_order_id() == request.get_order_id()


def note_insert_test_invalid_customer():
	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_customer_id(int(time.time()))\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.NoteInsert)


def note_insert_test_invalid_order():
	request = merchantapi.request.NoteInsert(helper.init_client())

	request.set_order_id(int(time.time()))\
		.set_note_text('API Inserted Customer Note')

	response = request.send()

	helper.validate_response_error(response, merchantapi.response.NoteInsert)
