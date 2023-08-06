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


def test_branch_property_version_list_load_query():
	"""
	Tests the BranchPropertyVersionList_Load_Query API Call
	"""

	branch_property_version_list_load_query_test_list_load()


def branch_property_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	branch = helper.create_branch('Production Copy', default_branch.get_color(), default_branch)

	assert branch is not None

	request = merchantapi.request.BranchPropertyVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchPropertyVersionListLoadQuery)

	assert len(response.get_branch_property_versions()) > 0

	for v in response.get_branch_property_versions():
		assert isinstance(v, merchantapi.model.BranchPropertyVersion)
