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


def test_branch_copy():
	"""
	Tests the Branch_Copy API Call
	"""

	branch_copy_test_copy()


def branch_copy_test_copy():
	helper.delete_branch('Production Copy 1')

	default_branch = helper.get_branch('Production')

	assert default_branch is not None

	create_request = merchantapi.request.BranchCreate(helper.init_client(), default_branch)
	create_request.set_name('Production Copy 1')
	create_request.set_color(default_branch.get_color())

	create_response = create_request.send()

	helper.validate_response_success(create_response, merchantapi.response.BranchCreate)

	request = merchantapi.request.BranchCopy(helper.init_client(), default_branch)

	request.set_destination_branch_id(create_response.get_branch().get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchCopy)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)

	assert response.get_changeset().get_id() > 0
	assert response.get_changeset().get_branch_id() > 0
