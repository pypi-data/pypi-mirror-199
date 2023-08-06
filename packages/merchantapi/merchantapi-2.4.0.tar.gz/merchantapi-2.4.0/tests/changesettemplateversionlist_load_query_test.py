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


def test_changeset_template_version_list_load_query():
	"""
	Tests the ChangesetTemplateVersionList_Load_Query API Call
	"""

	changeset_template_version_list_load_query_test_list_load()


def changeset_template_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None
	
	# Load a Changeset
	load_changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	load_changeset_response = load_changeset_request.send()

	helper.validate_response_success(load_changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert isinstance(load_changeset_response.get_changesets(), list)
	assert len(load_changeset_response.get_changesets()) > 0

	changeset = load_changeset_response.get_changesets()[0]

	assert isinstance(changeset, merchantapi.model.Changeset)

	request = merchantapi.request.ChangesetTemplateVersionListLoadQuery(helper.init_client(), changeset)
	
	assert changeset.get_id() == request.get_changeset_id()

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetTemplateVersionListLoadQuery)

	assert len(response.get_changeset_template_versions()) > 0

	for e in response.get_changeset_template_versions():
		assert isinstance(e, merchantapi.model.ChangesetTemplateVersion)
