"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Note_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/note_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class NoteDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, note: merchantapi.model.Note = None):
		"""
		NoteDelete Constructor.

		:param client: Client
		:param note: Note
		"""

		super().__init__(client)
		self.note_id = None
		if isinstance(note, merchantapi.model.Note):
			self.set_note_id(note.get_id())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Note_Delete'

	def get_note_id(self) -> int:
		"""
		Get Note_ID.

		:returns: int
		"""

		return self.note_id

	def set_note_id(self, note_id: int) -> 'NoteDelete':
		"""
		Set Note_ID.

		:param note_id: int
		:returns: NoteDelete
		"""

		self.note_id = note_id
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.NoteDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'NoteDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.NoteDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		data['Note_ID'] = self.note_id
		return data
