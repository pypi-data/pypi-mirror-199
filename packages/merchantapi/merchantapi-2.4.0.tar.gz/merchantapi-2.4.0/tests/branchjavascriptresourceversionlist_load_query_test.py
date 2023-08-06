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


def test_branch_javascript_resource_version_list_load_query():
	"""
	Tests the BranchJavaScriptResourceVersionList_Load_Query API Call
	"""

	branch_javascript_resource_version_list_load_query_test_list_load()


def branch_javascript_resource_version_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	request = merchantapi.request.BranchJavaScriptResourceVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchJavaScriptResourceVersionListLoadQuery)

	assert len(response.get_branch_javascript_resource_versions()) > 0

	for version in response.get_branch_javascript_resource_versions():
		assert isinstance(version, merchantapi.model.JavaScriptResourceVersion)
