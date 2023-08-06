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


def test_changeset_css_resource_version_list_load_query():
	"""
	Tests the ChangesetCSSResourceVersionList_Load_Query API Call
	"""

	helper.provision_store('ChangesetCSSResourceVersionList_Load_Query.xml')

	changeset_css_resource_version_list_load_query_test_list_load()


def changeset_css_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	branch = helper.create_branch('Production Copy', default_branch.get_color(), default_branch)

	assert branch is not None

	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client())
	changeset_request.set_branch_id(branch.get_id())

	changeset_response = changeset_request.send()

	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1
	assert changeset_response.get_changesets()[0].get_id() > 0

	request = merchantapi.request.ChangesetCSSResourceVersionListLoadQuery(helper.init_client())
	request.set_changeset_id(changeset_response.get_changesets()[0].get_id())

	request.set_filters(
		request.filter_expression()
			.like('code', 'ChangesetCSSResourceVersionListLoadQuery%')
	)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetCSSResourceVersionListLoadQuery)

	assert len(response.get_changeset_css_resource_versions()) == 6

	for version in response.get_changeset_css_resource_versions():
		assert isinstance(version, merchantapi.model.CSSResourceVersion)

		assert len(version.get_attributes()) > 0

		for attribute in version.get_attributes():
			assert isinstance(attribute, merchantapi.model.CSSResourceVersionAttribute)
