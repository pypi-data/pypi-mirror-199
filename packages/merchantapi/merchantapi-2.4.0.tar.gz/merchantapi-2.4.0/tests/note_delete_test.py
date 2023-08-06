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


def test_note_delete():
	"""
	Tests the Note_Delete API Call
	"""

	helper.provision_store('Note_Delete.xml')

	note_delete_test_deletion_by_business_account()
	note_delete_test_deletion_by_customer()


def note_delete_test_deletion_by_business_account():
	note = helper.get_note('business_title', 'NoteDeleteTest_BusinessAccount')

	assert isinstance(note, merchantapi.model.Note)

	request = merchantapi.request.NoteDelete(helper.init_client(), note)

	assert request.get_note_id() == note.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteDelete)


def note_delete_test_deletion_by_customer():
	note = helper.get_note('cust_login', 'NoteDeleteTest_Customer')

	assert isinstance(note, merchantapi.model.Note)

	request = merchantapi.request.NoteDelete(helper.init_client(), note)

	assert request.get_note_id() == note.get_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.NoteDelete)
