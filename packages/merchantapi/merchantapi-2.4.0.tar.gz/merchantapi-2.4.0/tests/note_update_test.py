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


def test_note_update():
	"""
	Tests the Note_Update API Call
	"""

	helper.provision_store('Note_Update.xml')

	note_update_test_update()


def note_update_test_update():
	notes_request = merchantapi.request.NoteListLoadQuery(helper.init_client())

	notes_request.set_filters(
		notes_request.filter_expression()
		.equal('cust_login', 'NoteUpdateTest_Customer')
		.or_equal('business_title', 'NoteUpdateTest_BusinessAccount')
		.or_equal('order_id', 978375551)
	)

	notes_response = notes_request.send()

	helper.validate_response_success(notes_response, merchantapi.response.NoteListLoadQuery)

	notes = notes_response.get_notes()

	assert isinstance(notes, list)
	assert len(notes) > 2

	request = merchantapi.request.NoteUpdate(helper.init_client())
	note_text = 'New Note Text %d' % int(time.time())

	request.set_note_id(notes[0].get_id())\
		.set_note_text(note_text)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteUpdate)

	note = helper.get_note('id', notes[0].get_id())

	assert isinstance(note, merchantapi.model.Note)
	assert note.get_note_text() == note_text
