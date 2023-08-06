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


def test_branch_template_version_list_load_query():
	"""
	Tests the BranchTemplateVersionList_Load_Query API Call
	"""

	branch_template_version_list_load_query_test_list_load()


def branch_template_version_list_load_query_test_list_load():
	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.BranchTemplateVersionListLoadQuery(helper.init_client(), branch)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchTemplateVersionListLoadQuery)

	assert len(response.get_branch_template_versions()) > 0

	for e in response.get_branch_template_versions():
		assert isinstance(e, merchantapi.model.BranchTemplateVersion)
