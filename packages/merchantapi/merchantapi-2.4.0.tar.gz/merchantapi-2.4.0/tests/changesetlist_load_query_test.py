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


def test_changeset_list_load_query():
	"""
	Tests the ChangesetTemplateVersionList_Load_Query API Call
	"""

	changeset_list_load_query_test_list_load()


def changeset_list_load_query_test_list_load():
	request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())

	request.set_branch_name('Production')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetListLoadQuery)

	assert len(response.get_changesets()) > 0

	for e in response.get_changesets():
		assert isinstance(e, merchantapi.model.Changeset)
