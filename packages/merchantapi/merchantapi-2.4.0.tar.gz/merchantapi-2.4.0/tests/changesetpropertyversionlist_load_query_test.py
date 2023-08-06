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


def test_changeset_property_version_list_load_query():
	"""
	Tests the ChangesetPropertyVersionList_Load_Query API Call
	"""

	changeset_property_version_list_load_query_test_list_load()


def changeset_property_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	branch = helper.create_branch('Production Copy', default_branch.get_color(), default_branch)

	assert branch is not None

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ChangesetPropertyVersionListLoadQuery(helper.init_client(), changeset_response.get_changesets()[0])

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetPropertyVersionListLoadQuery)

	assert len(response.get_changeset_property_versions()) > 0

	for v in response.get_changeset_property_versions():
		assert isinstance(v, merchantapi.model.ChangesetPropertyVersion)
