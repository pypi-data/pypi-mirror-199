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


def test_note_list_load_query():
	"""
	Tests the NoteList_Load_Query API Call
	"""

	helper.provision_store('NoteList_Load_Query.xml')

	note_list_load_query_test_list_load()


def note_list_load_query_test_list_load():
	request = merchantapi.request.NoteListLoadQuery(helper.init_client())

	request.set_filters(
		request.filter_expression()
		.equal('cust_login', 'NoteListLoadQuery_Customer_1')
		.and_equal('order_id', 10520)
		.and_equal('business_title', 'NoteListLoadQuery_BusinessAccount_1')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteListLoadQuery)

	assert isinstance(response.get_notes(), list)
	assert len(response.get_notes()) == 6

	for note in response.get_notes():
		assert isinstance(note, merchantapi.model.Note)
		assert note.get_business_title() == 'NoteListLoadQuery_BusinessAccount_1'
		assert note.get_customer_login() == 'NoteListLoadQuery_Customer_1'
		assert note.get_order_id() == 10520
		assert note.get_note_text() == 'This note should be customer NoteListLoadQuery_Customer_1 and order 10520 and business NoteListLoadQuery_BusinessAccount_1'
