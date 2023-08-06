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


def test_changeset_javascript_resource_version_list_load_query():
	"""
	Tests the ChangesetJavaScriptResourceVersionList_Load_Query API Call
	"""

	helper.provision_store('ChangesetJavaScriptResourceVersionList_Load_Query.xml')

	changeset_javascript_resource_version_list_load_query_test_list_load()


def changeset_javascript_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy 1')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	create_request = merchantapi.request.BranchCreate(helper.init_client(), default_branch)
	create_request.set_name('Production Copy 1')
	create_request.set_color(default_branch.get_color())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.BranchCreate)

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())
	changeset_request.set_branch_id(create_response.get_branch().get_id())

	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ChangesetJavaScriptResourceVersionListLoadQuery(helper.init_client())
	request.set_changeset_id(changeset_response.get_changesets()[0].get_id())

	request.set_filters(
		request.filter_expression()
			.like('code', 'ChangesetJavaScriptResourceVersionListLoadQuery%')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetJavaScriptResourceVersionListLoadQuery)

	assert len(response.get_changeset_javascript_resource_versions()) == 6

	for version in response.get_changeset_javascript_resource_versions():
		assert isinstance(version, merchantapi.model.ChangesetJavaScriptResourceVersion)

		assert len(version.get_attributes()) > 0

		for attribute in version.get_attributes():
			assert isinstance(attribute, merchantapi.model.JavaScriptResourceVersionAttribute)
